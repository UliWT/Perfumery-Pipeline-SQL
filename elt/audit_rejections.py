"""Persist source rows rejected by Silver business rules."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import text

from sql.connection import db_manager


REJECTION_QUERIES = (
    (
        "perfumes",
        "positive_price_and_name",
        """
        INSERT INTO audit.data_quality_issues
            (run_id, entity, source_id, rule_name, details)
        SELECT :run_id, 'perfumes', id::text,
               'positive_price_and_name',
               'price must be positive and name must be present'
          FROM staging.perfumes
         WHERE price IS NULL OR price <= 0
            OR name IS NULL OR btrim(name) = '' OR name = 'None'
        """,
    ),
    (
        "customers",
        "valid_email",
        """
        INSERT INTO audit.data_quality_issues
            (run_id, entity, source_id, rule_name, details)
        SELECT :run_id, 'customers', id::text,
               'valid_email', 'email does not match the expected format'
          FROM staging.customers
         WHERE email IS NULL
            OR email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}$'
        """,
    ),
    (
        "sales",
        "positive_quantity_and_foreign_keys",
        """
        INSERT INTO audit.data_quality_issues
            (run_id, entity, source_id, rule_name, details)
        SELECT :run_id, 'sales', id::text,
               'positive_quantity_and_foreign_keys',
               'quantity must be positive and critical ids must be present'
          FROM staging.sales
         WHERE quantity IS NULL OR quantity <= 0
            OR customer_id IS NULL OR perfume_id IS NULL OR location_id IS NULL
        """,
    ),
    (
        "inventory",
        "non_negative_stock",
        """
        INSERT INTO audit.data_quality_issues
            (run_id, entity, source_id, rule_name, details)
        SELECT :run_id, 'inventory', id::text,
               'non_negative_stock', 'current_stock cannot be negative or null'
          FROM staging.inventory
         WHERE current_stock IS NULL OR current_stock < 0
        """,
    ),
)


def record_rejections(run_id: UUID) -> None:
    """Record rejected source rows for one staging run."""
    engine = db_manager.get_engine()
    with engine.begin() as connection:
        for _, _, query in REJECTION_QUERIES:
            connection.execute(text(query), {"run_id": run_id})


if __name__ == "__main__":
    raise SystemExit("Call record_rejections(run_id) from the pipeline orchestrator.")

