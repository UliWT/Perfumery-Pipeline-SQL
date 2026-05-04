import pandas as pd
from datetime import datetime
from deltalake.writer import write_deltalake
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sql.connection import db_manager
from src.config import BRONZE_PATH, RAW_SCHEMA, TABLES

def ingest_to_bronze():
    """
    Ingests tables from PostgreSQL 'raw' schema into Delta Lake Bronze layer.
    """
    print(f"--- Starting Bronze Ingestion ---")
    
    # Get engine from our connection manager
    try:
        engine = db_manager.get_engine()
    except Exception as e:
        print(f"Failed to connect to PostgreSQL. Error: {e}")
        return

    # Ensure base bronze directory exists
    if not os.path.exists(BRONZE_PATH):
        os.makedirs(BRONZE_PATH)

    for table_name in TABLES:
        try:
            # Read data from Postgres
            query = f"SELECT * FROM {RAW_SCHEMA}.{table_name}"
            df = pd.read_sql(query, engine)
            
            # Add metadata column
            df['processed_at'] = datetime.now()
            
            # Define output path for the Delta table
            output_path = os.path.join(BRONZE_PATH, table_name)
            
            # Write to Delta Lake (overwrite mode as per design)
            write_deltalake(output_path, df, mode='overwrite')
            
        except Exception as e:
            print(f"[{table_name}] Error during ingestion: {e}")

    print(f"Bronze Ingestion: OK")

if __name__ == "__main__":
    ingest_to_bronze()
