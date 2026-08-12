"""Load source tables into PostgreSQL staging without transforming them."""

from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID, uuid4

from sqlalchemy import text

from sql.connection import db_manager


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TABLES = (
    "brands",
    "perfumes",
    "customers",
    "locations",
    "sales",
    "inventory",
)


def _execute_sql_file(connection, path: Path) -> None:
    """Execute a versioned SQL file through the active PostgreSQL connection."""
    connection.exec_driver_sql(path.read_text(encoding="utf-8"))


def prepare_database(connection) -> None:
    """Create ELT metadata objects idempotently."""
    _execute_sql_file(connection, PROJECT_ROOT / "sql/elt/00_create_schemas.sql")
    _execute_sql_file(connection, PROJECT_ROOT / "sql/elt/01_create_staging.sql")


def _start_run(connection, run_id: UUID, started_at: datetime) -> None:
    connection.execute(
        text(
            """
            INSERT INTO audit.pipeline_runs
                (run_id, pipeline_name, started_at, status)
            VALUES (:run_id, :pipeline_name, :started_at, 'running')
            """
        ),
        {
            "run_id": run_id,
            "pipeline_name": "perfumery_elt",
            "started_at": started_at,
        },
    )


def _finish_run(
    connection,
    run_id: UUID,
    status: str,
    finished_at: datetime,
    error_message: str | None = None,
) -> None:
    connection.execute(
        text(
            """
            UPDATE audit.pipeline_runs
               SET finished_at = :finished_at,
                   status = :status,
                   error_message = :error_message
             WHERE run_id = :run_id
            """
        ),
        {
            "run_id": run_id,
            "finished_at": finished_at,
            "status": status,
            "error_message": error_message,
        },
    )


def load_staging(full_refresh: bool = True) -> UUID:
    """Copy raw tables to staging and return the execution id.

    A full refresh is intentional for this first ELT step. Incremental loading
    will be added after the source change strategy is defined.
    """
    engine = db_manager.get_engine()
    run_id = uuid4()
    started_at = datetime.now(timezone.utc)

    with engine.begin() as connection:
        prepare_database(connection)
        _start_run(connection, run_id, started_at)

        try:
            if full_refresh:
                for table in TABLES:
                    connection.execute(text(f"TRUNCATE TABLE staging.{table}"))

            for table in TABLES:
                columns = connection.execute(
                    text(
                        """
                        SELECT column_name
                          FROM information_schema.columns
                         WHERE table_schema = 'raw'
                           AND table_name = :table_name
                         ORDER BY ordinal_position
                        """
                    ),
                    {"table_name": table},
                ).scalars().all()

                if not columns:
                    raise RuntimeError(f"Source table raw.{table}")

                column_list = ", ".join(columns)
                connection.execute(
                    text(
                        f"""
                        INSERT INTO staging.{table}
                            ({column_list}, _ingested_at, _run_id)
                        SELECT {column_list}, :ingested_at, :run_id
                          FROM raw.{table}
                        """
                    ),
                    {"ingested_at": started_at, "run_id": run_id},
                )

            _finish_run(
                connection,
                run_id,
                "success",
                datetime.now(timezone.utc),
            )
        except Exception as exc:
            _finish_run(
                connection,
                run_id,
                "failed",
                datetime.now(timezone.utc),
                str(exc),
            )
            raise

    return run_id


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-refresh",
        action="store_true",
        help="Do not clear staging before inserting; use only with an incremental strategy.",
    )
    args = parser.parse_args()
    run_id = load_staging(full_refresh=not args.no_refresh)
    print(f"Staging loaded successfully. run_id={run_id}")


if __name__ == "__main__":
    main()

