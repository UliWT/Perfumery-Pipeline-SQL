import pandas as pd
from deltalake import DeltaTable
from deltalake.writer import write_deltalake
import os
import sys

# Path and import configuration
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import BRONZE_PATH, SILVER_PATH, TABLES, ENRICHED_TABLES, logger

def read_from_bronze(table_name):
    """Reads a table from the Bronze layer."""
    path = os.path.join(BRONZE_PATH, table_name)
    try:
        return DeltaTable(path).to_pandas()
    except Exception as e:
        logger.error(f"Error reading {table_name} from Bronze: {e}")
        return pd.DataFrame()

def save_to_silver(df, table_name):
    """Persists a DataFrame to the Silver layer."""
    try:
        path = os.path.join(SILVER_PATH, table_name)
        write_deltalake(path, df, mode='overwrite', schema_mode='overwrite')
        logger.info(f"Table '{table_name}' successfully persisted in Silver.")
    except Exception as e:
        logger.error(f"Error saving {table_name} to Silver: {e}")

def basic_cleaning(df, table_name):
    """
    Base technical cleaning:
    1. Removes duplicates.
    2. Trims whitespace from strings.
    3. Resets the index.
    """
    if df.empty:
        return df
    
    initial_rows = len(df)
    
    # 1. Remove exact duplicates
    df = df.drop_duplicates().reset_index(drop=True)
    
    # 2. Trim whitespace in text columns
    str_cols = df.select_dtypes(include=['object']).columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()
    
    # 3. Duplicate reporting
    diff = initial_rows - len(df)
    if diff > 0:
        logger.warning(f"[{table_name}] Removed {diff} duplicate rows.")
    
    return df

def apply_business_rules(df, table_name):
    """
    Applies entity-specific business rules.
    Filters records that do not meet minimum quality criteria.
    """
    if df.empty:
        return df

    initial_count = len(df)

    if table_name == "perfumes":
        # Rule: Price must be positive and name must not be null
        df = df[df['price'] > 0]
        df = df[df['name'].notna() & (df['name'] != 'None')]

    elif table_name == "sales":
        # Rule: Quantity must be greater than 0
        df = df[df['quantity'] > 0]
        # Validate that critical IDs exist
        df = df.dropna(subset=['customer_id', 'perfume_id', 'location_id'])

    elif table_name == "customers":
        # Rule: Email must have a valid basic format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        df = df[df['email'].str.contains(email_regex, na=False, regex=True)]

    elif table_name == "inventory":
        # Rule: Stock cannot be negative
        df = df[df['current_stock'] >= 0]

    dropped = initial_count - len(df)
    if dropped > 0:
        logger.warning(f"[{table_name}] Business Rules: Discarded {dropped} rows due to inconsistencies.")
    
    return df.reset_index(drop=True)

def transform_bronze_to_silver():
    """
    Silver layer orchestrator: Bronze -> Cleaning -> Business Rules -> Enrichment -> Silver.
    
    TODO: Transition to incremental processing. Instead of a full overwrite,
    only process records added to Bronze since the last run. This will involve 
    using Delta Lake MERGE operations for base tables and CDC-like logic for enrichments.
    """
    logger.info("Starting Bronze -> Silver Transformation...")
    
    if not os.path.exists(SILVER_PATH):
        os.makedirs(SILVER_PATH)

    data = {}
    
    # --- 1. BASE TABLE PROCESSING ---
    for table in TABLES:
        logger.info(f"Processing base table: {table}")
        
        df_raw = read_from_bronze(table)
        if df_raw.empty:
            logger.warning(f"Table {table} empty in Bronze. Skipping...")
            data[table] = df_raw
            continue
            
        # Technical cleaning and business rules
        df_clean = basic_cleaning(df_raw, table)
        df_final = apply_business_rules(df_clean, table)
        
        # Save the clean base version
        save_to_silver(df_final, table)
        data[table] = df_final

    # --- 2. ENRICHED TABLE GENERATION ---
    logger.info("Generating enriched tables (Joins)...")
    
    enrichment_tasks = [
        ("perfumes_enriched", create_perfumes_enriched, ['perfumes', 'brands']),
        ("sales_enriched", create_sales_enriched, ['sales', 'perfumes', 'locations', 'customers', 'brands']),
        ("customers_enriched", create_customers_enriched, ['customers', 'locations']),
        ("inventory_enriched", create_inventory_enriched, ['inventory', 'perfumes', 'brands'])
    ]

    for target_table, func, dependencies in enrichment_tasks:
        try:
            # Verify that all dependencies have data
            if all(not data[dep].empty for dep in dependencies):
                args = [data[dep] for dep in dependencies]
                df_enriched = func(*args)
                save_to_silver(df_enriched, target_table)
            else:
                logger.warning(f"Skipping {target_table} due to empty dependencies.")
        except Exception as e:
            logger.error(f"Critical failure generating {target_table}: {e}")

    logger.info("Silver layer completion successful.")

# --- ENRICHMENT FUNCTIONS ---

def create_perfumes_enriched(perfumes_df, brands_df):
    """Joins perfumes with brands."""
    b_df = brands_df[['id', 'name', 'country']].rename(
        columns={'id': 'brand_id', 'name': 'brand_name'}
    )
    enriched = pd.merge(perfumes_df, b_df, on='brand_id', how='inner')
    final_cols = ['brand_name', 'name', 'perfume_type', 'size_ml', 'price', 'country']
    return enriched[final_cols]

def create_sales_enriched(sales_df, perfumes_df, locations_df, customers_df, brands_df):
    """Mega Join of sales with all related dimensions."""
    c_df = customers_df[['id', 'first_name', 'last_name']].rename(columns={'id': 'customer_id'})
    l_df = locations_df[['id', 'name', 'state']].rename(columns={'id': 'location_id', 'name': 'location_name'})
    p_df = perfumes_df[['id', 'name', 'brand_id', 'price']].rename(columns={'id': 'perfume_id', 'name': 'perfume_name'})
    b_df = brands_df[['id', 'name']].rename(columns={'id': 'brand_id', 'name': 'brand_name'})
    
    df = sales_df.merge(c_df, on='customer_id', how='left')
    df = df.merge(l_df, on='location_id', how='left')
    df = df.merge(p_df, on='perfume_id', how='left')
    df = df.merge(b_df, on='brand_id', how='left')
    
    final_cols = [
        'sale_date', 'first_name', 'last_name', 'location_name', 
        'state', 'brand_name', 'perfume_name', 'quantity', 'price'
    ]
    return df[final_cols]

def create_customers_enriched(customers_df, locations_df):
    """Joins customers with their location."""
    # Handle potential inconsistency in source column names (location vs location_id)
    if 'location' in customers_df.columns and 'location_id' not in customers_df.columns:
        customers_df = customers_df.rename(columns={'location': 'location_id'})

    l_df = locations_df[['id', 'name', 'state']].rename(
        columns={'id': 'location_id', 'name': 'location_name'}
    )
    
    # Ensure compatible types for the merge
    customers_df['location_id'] = customers_df['location_id'].astype(int)
    l_df['location_id'] = l_df['location_id'].astype(int)

    enriched = pd.merge(customers_df, l_df, on='location_id', how='inner')
    final_cols = ['first_name', 'last_name', 'email', 'location_name', 'state']
    return enriched[final_cols]

def create_inventory_enriched(inventory_df, perfumes_df, brands_df):
    """Joins inventory with perfumes and brands."""
    p_df = perfumes_df[['id', 'name', 'brand_id']].rename(columns={'id': 'perfume_id', 'name': 'perfume_name'})
    b_df = brands_df[['id', 'name']].rename(columns={'id': 'brand_id', 'name': 'brand_name'})
    df = inventory_df.merge(p_df, on='perfume_id', how='left')
    df = df.merge(b_df, on='brand_id', how='left')
    final_cols = ['brand_name', 'perfume_name', 'current_stock']
    return df[final_cols]

if __name__ == "__main__":
    transform_bronze_to_silver()
