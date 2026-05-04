import pandas as pd
from deltalake import DeltaTable
from deltalake.writer import write_deltalake
import os
import sys

# Configuración de rutas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import BRONZE_PATH, SILVER_PATH, TABLES

def read_from_bronze(table_name):
    """Lee una tabla de la capa Bronze."""
    path = os.path.join(BRONZE_PATH, table_name)
    try:
        return DeltaTable(path).to_pandas()
    except Exception as e:
        print(f"[!] Error leyendo {table_name} de Bronze: {e}")
        return pd.DataFrame()

def save_to_silver(df, table_name):
    """Guarda un DataFrame en la capa Silver."""
    path = os.path.join(SILVER_PATH, table_name)
    write_deltalake(path, df, mode='overwrite')
    print(f"[OK] Tabla '{table_name}' guardada en Silver.")

def basic_cleaning(df):
    """
    Limpieza base:
    1. Elimina duplicados.
    2. Elimina filas con nulos.
    3. Resetea el índice empezando desde 1.
    """
    if df.empty:
        return df
    
    # 1. Redundancias (duplicados)
    df = df.drop_duplicates().reset_index(drop=True)
    
    # 2. Datos nulos (limpieza agresiva por ahora)
    df = df.dropna()
    
    # 3. Index a partir de 1
    df.index = df.index + 1
    
    return df

def transform_bronze_to_silver():
    """Orquestador de la capa Silver."""
    if not os.path.exists(SILVER_PATH):
        os.makedirs(SILVER_PATH)

    # --- 1. PROCESAMIENTO DE TABLAS BASE ---
    data = {}
    for table in TABLES:
        print(f"-> Procesando base: {table}")
        df_raw = read_from_bronze(table)
        df_clean = basic_cleaning(df_raw)
        
        # Guardamos la versión limpia básica
        save_to_silver(df_clean, table)
        data[table] = df_clean

    # --- 2. TABLAS ENRIQUECIDAS ---
    
    print("\n>>> Generando tablas enriquecidas...")
    
    # 1. Perfumes Enriched
    perfumes_enriched = create_perfumes_enriched(data['perfumes'], data['brands'])
    if not perfumes_enriched.empty:
        save_to_silver(perfumes_enriched, "perfumes_enriched")
    
    # 2. Sales Enriched
    sales_enriched = create_sales_enriched(data['sales'], data['perfumes'], data['locations'], data['customers'], data['brands'])
    if not sales_enriched.empty:
        save_to_silver(sales_enriched, "sales_enriched")
    
    # 3. Customers Enriched
    customers_enriched = create_customers_enriched(data['customers'], data['locations'])
    if not customers_enriched.empty:
        save_to_silver(customers_enriched, "customers_enriched")

    #4. Inventory Enriched
    inventory_enriched = create_inventory_enriched(data['inventory'], data['perfumes'], data['brands'])
    if not inventory_enriched.empty:
        save_to_silver(inventory_enriched, "inventory_enriched")

# --- ESPACIO PARA TUS FUNCIONES DE JOIN ---

def create_perfumes_enriched(perfumes_df, brands_df):
    """
    Traducido de tu SQL:
    select b.name as brand_name, p.name, p.perfume_type, p.size_ml, p.price, b.country
    from brands b join perfumes p on b.id = p.brand_id
    """
    # Renombramos para evitar colisiones y que quede claro
    brands_subset = brands_df[['id', 'name', 'country']].rename(columns={'name': 'brand_name', 'id': 'brand_id'})
    
    # Join
    enriched = pd.merge(perfumes_df, brands_subset, on='brand_id', how='inner')
    
    # Selección de columnas según tu SQL
    final_cols = ['brand_name', 'name', 'perfume_type', 'size_ml', 'price', 'country']
    return enriched[final_cols]

def create_sales_enriched(sales_df, perfumes_df, locations_df, customers_df, brands_df):
    """
    Mega Join traducido de tu SQL:
    select c.first_name, c.last_name, l.name, l.state, b.name, p.name, s.quantity, s.sale_date
    """
    # Mapeo de columnas corregido (Pandas solo agrega sufijos si hay colisión)
    # Vamos a buscar las columnas por lo que contienen
    
    # 1. Sales + Customers
    df = pd.merge(sales_df, customers_df, left_on='customer_id', right_on='id', suffixes=('', '_cust'))
    
    # 2. + Locations (del cliente)
    # Si 'name' ya existe de customers, acá sí habrá colisión
    df = pd.merge(df, locations_df, left_on='location', right_on='id', suffixes=('', '_loc'))
    
    # 3. + Perfumes
    df = pd.merge(df, perfumes_df, left_on='perfume_id', right_on='id', suffixes=('', '_perf'))
    
    # 4. + Brands (del perfume)
    df = pd.merge(df, brands_df, left_on='brand_id', right_on='id', suffixes=('', '_brand'))
    
    # Intentamos detectar los nombres reales de las columnas (pueden variar según el orden de los merges)
    # customers_df suele traer 'first_name', 'last_name'
    # locations_df trae 'name' -> name_loc
    # perfumes_df trae 'name' -> name_perf
    # brands_df trae 'name' -> name_brand
    
    # Mapeo flexible
    cols_map = {}
    if 'first_name' in df.columns: cols_map['first_name'] = 'first_name'
    if 'last_name' in df.columns: cols_map['last_name'] = 'last_name'
    if 'name_loc' in df.columns: cols_map['name_loc'] = 'location_name'
    elif 'name' in df.columns: cols_map['name'] = 'location_name' # Fallback
    
    if 'state' in df.columns: cols_map['state'] = 'state'
    
    if 'name_brand' in df.columns: cols_map['name_brand'] = 'brand_name'
    if 'name_perf' in df.columns: cols_map['name_perf'] = 'perfume_name'
    if 'price' in df.columns: cols_map['price'] = 'price'
    if 'quantity' in df.columns: cols_map['quantity'] = 'quantity'
    if 'sale_date' in df.columns: cols_map['sale_date'] = 'sale_date'

    return df[list(cols_map.keys())].rename(columns=cols_map)

def create_customers_enriched(customers_df, locations_df):
    locs = locations_df[['id', 'name', 'state']].rename(
        columns={'name': 'country', 'id': 'location'}
    )

    enriched = pd.merge(customers_df, locs, on='location', how='inner')

    final_cols=['first_name', 'last_name', 'email', 'country', 'state']
    return enriched[final_cols]

def create_inventory_enriched(inventory_df, perfumes_df, brands_df):
    """
    Une inventario con perfumes y marcas para tener la vista completa.
    """
    if inventory_df.empty or perfumes_df.empty or brands_df.empty:
        return pd.DataFrame()

    # 1. Unimos inventario con perfumes
    df = pd.merge(inventory_df, perfumes_df, left_on='perfume_id', right_on='id')
    
    # 2. Unimos con marcas
    df = pd.merge(df, brands_df, left_on='brand_id', right_on='id', suffixes=('', '_brand'))

    # 3. Seleccionamos columnas finales (usando los nombres que deja el merge)
    final_cols = ['name_brand', 'name', 'size_ml', 'current_stock']
    
    # Filtramos solo las que existen para evitar errores
    existing_cols = [c for c in final_cols if c in df.columns]
    
    return df[existing_cols].rename(columns={'name_brand': 'brand', 'name': 'perfume'})

if __name__ == "__main__":
    transform_bronze_to_silver()
