"""Execute Gold SQL models against PostgreSQL."""

from __future__ import annotations

from pathlib import Path

from sql.connection import db_manager


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_gold_models() -> None:
    path = PROJECT_ROOT / "sql/elt/03_build_gold.sql"
    engine = db_manager.get_engine()
    with engine.begin() as connection:
        connection.exec_driver_sql(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    run_gold_models()
    print("Gold models built successfully.")

