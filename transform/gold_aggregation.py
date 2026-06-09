import pandas as pd
from deltalake import DeltaTable
from deltalake.writer import write_deltalake
import os
import sys

# Path and import configuration
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import SILVER_PATH, GOLD_PATH, logger

def read_silver_table(table_name):
    """Reads a table from the Silver layer."""
    path = os.path.join(SILVER_PATH, table_name)
    try:
        return DeltaTable(path).to_pandas()
    except Exception as e:
        logger.error(f"Error reading {table_name} from Silver: {e}")
        return pd.DataFrame()

def save_to_gold(df, table_name):
    """Persists a DataFrame to the Gold layer."""
    try:
        if not os.path.exists(GOLD_PATH):
            os.makedirs(GOLD_PATH)
        path = os.path.join(GOLD_PATH, table_name)
        write_deltalake(path, df, mode='overwrite', schema_mode='overwrite')
        logger.info(f"Gold table '{table_name}' successfully generated.")
    except Exception as e:
        logger.error(f"Error generating Gold table '{table_name}': {e}")

def aggregate_gold():
    """Gold layer orchestrator: Generates business aggregates."""
    logger.info("Starting Gold Aggregations (Business Layer)...")
    
    # Load the main enriched fact table
    df_sales = read_silver_table("sales_enriched")
    
    if df_sales.empty:
        logger.warning("No data found in sales_enriched to process. Aborting Gold.")
        return

    # --- 1. REVENUE BY BRAND ---
    logger.info("Calculating Revenue by Brand...")
    df_sales['revenue'] = df_sales['quantity'] * df_sales['price']
    
    revenue_by_brand = df_sales.groupby('brand_name').agg(
        total_revenue=('revenue', 'sum')
    ).reset_index().sort_values(by='total_revenue', ascending=False)
    
    save_to_gold(revenue_by_brand, "revenue_by_brand")

    # --- 2. TOP SELLING PERFUMES ---
    logger.info("Calculating Top Selling Perfumes...")
    top_selling_perfumes = df_sales.groupby('perfume_name').agg(
        total_quantity=('quantity', 'sum')
    ).reset_index().sort_values(by='total_quantity', ascending=False)
    
    save_to_gold(top_selling_perfumes, "top_selling_perfumes")

    # --- 3. REVENUE BY LOCATION ---
    logger.info("Calculating Revenue by Location...")
    revenue_by_location = df_sales.groupby('location_name').agg(
        total_revenue=('revenue', 'sum')
    ).reset_index().sort_values(by='total_revenue', ascending=False)
    
    save_to_gold(revenue_by_location, "revenue_by_location")

    logger.info("Gold layer completion successful.")

if __name__ == "__main__":
    aggregate_gold()
