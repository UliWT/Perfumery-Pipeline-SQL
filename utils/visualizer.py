import pandas as pd
from deltalake import DeltaTable
import os

def format_dataframe(df, table_name):
    """Cleans the DataFrame for display purposes."""
    # Remove 'processed_at' unless it's the sales table
    if table_name.lower() != 'sales' and 'processed_at' in df.columns:
        df = df.drop(columns=['processed_at'])
    
    # Remove internal delta/pandas indices if they exist
    cols_to_drop = [col for col in df.columns if col.startswith('__index_level')]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
        
    return df

def show_table(base_path, table_name, layer_label):
    """Reads and displays a specific table from a layer."""
    path = os.path.join(base_path, table_name)
    
    if not os.path.exists(path):
        print(f"\n[!] Table '{table_name}' not found in {layer_label} layer.")
        return

    try:
        df = DeltaTable(path).to_pandas()
        df = format_dataframe(df, table_name)
        
        print(f"\n>>> LAYER: {layer_label.upper()} | TABLE: {table_name.upper()} ({len(df)} rows)")
        print("-" * 60)
        # In Big Data scenarios, we only show a sample
        print(df.head(20).to_string(index=False))
        print("-" * 60)
    except Exception as e:
        print(f"Error displaying {table_name}: {e}")

def show_layer_summary(base_path, layer_label, tables):
    """Displays a summary of multiple tables in a layer."""
    print(f"\n" + "="*60)
    print(f"      {layer_label.upper()} LAYER PREVIEW")
    print("="*60)
    
    for table in tables:
        show_table(base_path, table, layer_label)
    
    print("\n" + "="*60)
