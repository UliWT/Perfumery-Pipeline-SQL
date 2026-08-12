"""Run the PostgreSQL ELT pipeline in dependency order."""

from __future__ import annotations

from elt.load_staging import load_staging
from elt.audit_rejections import record_rejections
from elt.run_gold_models import run_gold_models
from elt.run_sql_models import run_silver_models
from elt.run_quality_checks import run_quality_checks


def run_pipeline() -> None:
    run_id = load_staging()
    record_rejections(run_id)
    run_silver_models()
    run_gold_models()
    run_quality_checks()
    print(f"ELT pipeline completed successfully. run_id={run_id}")


if __name__ == "__main__":
    run_pipeline()

