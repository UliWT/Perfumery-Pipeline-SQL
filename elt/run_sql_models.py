"""Execute versioned SQL models against PostgreSQL."""

from __future__ import annotations

from pathlib import Path

from sql.connection import db_manager


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_silver_models() -> None:
    path = PROJECT_ROOT / "sql/elt/02_build_silver.sql"
    engine = db_manager.get_engine()
    with engine.begin() as connection:
        sql_script = path.read_text(encoding="utf-8").replace("%", "%%")
        connection.exec_driver_sql(sql_script)


if __name__ == "__main__":
    run_silver_models()
    print("Silver models built successfully.")

