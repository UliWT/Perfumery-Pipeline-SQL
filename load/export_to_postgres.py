import pandas as pd
from deltalake import DeltaTable
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sql.connection import db_manager
from src.config import GOLD_PATH, ANALYTICS_SCHEMA

def export_gold_to_postgres():
    """
    Reads all Gold tables from Delta Lake and exports them to the PostgreSQL 'analytics' schema.
    """
    print("--- Starting Gold Export to Postgres ---")
    
    try:
        engine = db_manager.get_engine()
    except Exception as e:
        print(f"Failed to connect to PostgreSQL. Error: {e}")
        return
    
    # Identify Gold tables to export
    if not os.path.exists(GOLD_PATH):
        print(f"Gold path {GOLD_PATH} does not exist. Run aggregation first.")
        return

    # Filter directories that look like Delta tables (contain _delta_log)
    gold_tables = []
    for d in os.listdir(GOLD_PATH):
        table_path = os.path.join(GOLD_PATH, d)
        if os.path.isdir(table_path) and os.path.exists(os.path.join(table_path, "_delta_log")):
            gold_tables.append(d)
    
    if not gold_tables:
        print("No Gold tables found to export.")
        return

    for table_name in gold_tables:
        try:
            path = os.path.join(GOLD_PATH, table_name)
            dt = DeltaTable(path)
            df = dt.to_pandas()
            
            # Using 'replace' to ensure schema updates if changed, though 'append' could be used for history
            df.to_sql(
                name=table_name,
                con=engine,
                schema=ANALYTICS_SCHEMA,
                if_exists='replace',
                index=False
            )
            
        except Exception as e:
            print(f"[{table_name}] Error during export: {e}")

    print("Gold Export: OK")

if __name__ == "__main__":
    export_gold_to_postgres()
