import sys
import os
from extract.ingest_to_bronze import ingest_to_bronze
from transform.silver_transformation import transform_bronze_to_silver
from transform.gold_aggregation import aggregate_gold
from load.export_to_postgres import export_gold_to_postgres
from src.config import SILVER_PATH, GOLD_PATH, TABLES
from utils.visualizer import show_layer_summary, show_table

def run_pipeline():
    """Runs the full ETL process."""
    print("\n>>> Executing Full Pipeline...")
    ingest_to_bronze()
    transform_bronze_to_silver()
    aggregate_gold()
    export_gold_to_postgres()
    print(">>> Pipeline Execution: SUCCESS\n")

def main():
    """
    Orchestrator for the Perfumeria Data Pipeline.
    Supports running the full pipeline or inspecting specific tables.
    Usage:
      python main.py              # Runs the full pipeline
      python main.py --silver     # Shows Silver layer summary
      python main.py --gold       # Shows Gold layer summary
      python main.py --table NAME # Shows a specific table (default Gold)
    """
    
    if len(sys.argv) == 1:
        run_pipeline()
        # Default view after full run
        show_layer_summary(GOLD_PATH, "Gold", ["revenue_by_brand", "top_selling_perfumes"])
        return

    arg = sys.argv[1].lower()

    if arg == "--silver":
        show_layer_summary(SILVER_PATH, "Silver", ["perfumes_enriched", "brands", "sales"])
    
    elif arg == "--gold":
        show_layer_summary(GOLD_PATH, "Gold", ["revenue_by_brand", "top_selling_perfumes", "revenue_by_location"])
    
    elif arg == "--table" and len(sys.argv) > 2:
        table_name = sys.argv[2]
        # Search in Gold first, then Silver
        if os.path.exists(os.path.join(GOLD_PATH, table_name)):
            show_table(GOLD_PATH, table_name, "Gold")
        elif os.path.exists(os.path.join(SILVER_PATH, table_name)):
            show_table(SILVER_PATH, table_name, "Silver")
        else:
            print(f"[!] Table '{table_name}' not found in Silver or Gold layers.")
    
    else:
        print("Invalid arguments. Use --silver, --gold, or --table [name].")

if __name__ == "__main__":
    main()
