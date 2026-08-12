"""Run SQL data quality checks and fail on the first failed check."""

from __future__ import annotations

from pathlib import Path

from sql.connection import db_manager


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_quality_checks() -> None:
    path = PROJECT_ROOT / "sql/elt/04_quality_checks.sql"
    statements = [
        statement.strip()
        for statement in path.read_text(encoding="utf-8").split(";")
        if statement.strip() and not statement.lstrip().startswith("--")
    ]

    engine = db_manager.get_engine()
    failures = []
    with engine.connect() as connection:
        for statement in statements:
            result = connection.exec_driver_sql(statement.replace("%", "%%"))
            check_name, passed, invalid_rows = result.one()
            print(f"{check_name}: {'PASS' if passed else 'FAIL'} ({invalid_rows} rows)")
            if not passed:
                failures.append(check_name)

    if failures:
        raise RuntimeError(f"Quality checks failed: {', '.join(failures)}")


if __name__ == "__main__":
    run_quality_checks()

