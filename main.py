import sys
import os
import logging
from extract.ingest_to_bronze import ingest_to_bronze
from transform.silver_transformation import transform_bronze_to_silver
from transform.gold_aggregation import aggregate_gold
from load.export_to_postgres import export_gold_to_postgres
from src.config import SILVER_PATH, GOLD_PATH, TABLES, ENRICHED_TABLES, GOLD_METRICS, logger
from utils.visualizer import show_layer_summary, show_table

def run_pipeline():
    """Runs the full ETL process."""
    logger.info(">>> Starting Full Pipeline Execution...")
    try:
        ingest_to_bronze()
        transform_bronze_to_silver()
        aggregate_gold()
        export_gold_to_postgres()
        logger.info(">>> Pipeline Execution: SUCCESSFUL")
    except Exception as e:
        logger.error(f">>> Pipeline FAILED: {str(e)}", exc_info=True)

def main():
    """
    Orchestrator for the Niche Perfumery Data Pipeline.
    Supports running the full pipeline or inspecting specific tables.
    """

    if len(sys.argv) == 1:
        run_pipeline()
        # Default view after full run
        show_layer_summary(GOLD_PATH, "Gold", GOLD_METRICS)
        return

    arg = sys.argv[1].lower()

    if arg == "--silver":
        show_layer_summary(SILVER_PATH, "Silver", ENRICHED_TABLES)

    elif arg == "--gold":
        show_layer_summary(GOLD_PATH, "Gold", GOLD_METRICS)

    elif arg == "--table" and len(sys.argv) > 2:
        table_name = sys.argv[2]
        # Search for the table in both Gold and Silver layers
        if os.path.exists(os.path.join(GOLD_PATH, table_name)):
            show_table(GOLD_PATH, table_name, "Gold")
        elif os.path.exists(os.path.join(SILVER_PATH, table_name)):
            show_table(SILVER_PATH, table_name, "Silver")
        else:
            logger.warning(f"Table '{table_name}' not found in any layer.")

    else:
        logger.info("Usage: python main.py [--silver | --gold | --table NAME]")

if __name__ == "__main__":
    main()
