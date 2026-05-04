import pandas as pd
from deltalake import DeltaTable
from deltalake.writer import write_deltalake
import os
import sys

# Configuración de rutas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import SILVER_PATH, GOLD_PATH

def read_silver_table(table_name):
    """Lee una tabla de la capa Silver."""
    path = os.path.join(SILVER_PATH, table_name)
    try:
        return DeltaTable(path).to_pandas()
    except Exception as e:
        print(f"[!] Error leyendo {table_name} de Silver: {e}")
        return pd.DataFrame()

def save_to_gold(df, table_name):
    """Guarda un DataFrame en la capa Gold."""
    if not os.path.exists(GOLD_PATH):
        os.makedirs(GOLD_PATH)
    path = os.path.join(GOLD_PATH, table_name)
    write_deltalake(path, df, mode='overwrite', overwrite_schema=True)
    print(f"[OK] Tabla Gold '{table_name}' generada.")

def aggregate_gold():
    """Orquestador de la capa Gold."""
    print("\n--- Iniciando Agregaciones Gold ---")
    
    # Cargamos la tabla principal de hechos enriquecida
    df_sales = read_silver_table("sales_enriched")
    
    if df_sales.empty:
        print("[!] No hay datos en sales_enriched para procesar.")
        return

    # --- 1. REVENUE BY BRAND ---
    # Objetivo: brand_name | total_revenue
    print("-> Calculando Revenue por Marca...")
    # [TU CÓDIGO AQUÍ]
    # Tip: 
    # df_sales['revenue'] = ...
    # revenue_by_brand = df_sales.groupby(...).agg(total_revenue=('revenue', 'sum')).reset_index()
    # save_to_gold(revenue_by_brand, "revenue_by_brand")

    # --- 2. TOP SELLING PERFUMES ---
    # Objetivo: perfume_name | total_quantity
    print("-> Calculando Top Perfumes...")
    # [TU CÓDIGO AQUÍ]

    # --- 3. REVENUE BY LOCATION ---
    # Objetivo: location_name | total_revenue
    print("-> Calculando Revenue por Locación...")
    # [TU CÓDIGO AQUÍ]

if __name__ == "__main__":
    aggregate_gold()
