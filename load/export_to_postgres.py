import pandas as pd
from deltalake import DeltaTable
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sql.connection import db_manager
from src.config import GOLD_PATH, ANALYTICS_SCHEMA, logger

def export_gold_to_postgres():
    """
    Reads all Gold tables from Delta Lake and exports them to the PostgreSQL 'analytics' schema.
    """
    logger.info("Iniciando Exportación de Capa Gold a PostgreSQL (Analytics)...")
    
    try:
        engine = db_manager.get_engine()
    except Exception as e:
        logger.error(f"Falla crítica: No se pudo conectar a PostgreSQL. Error: {e}")
        return
    
    if not os.path.exists(GOLD_PATH):
        logger.error(f"La ruta de Gold '{GOLD_PATH}' no existe. Ejecutá las agregaciones primero.")
        return

    # Filtrar directorios que parecen ser tablas Delta
    gold_tables = []
    for d in os.listdir(GOLD_PATH):
        table_path = os.path.join(GOLD_PATH, d)
        if os.path.isdir(table_path) and os.path.exists(os.path.join(table_path, "_delta_log")):
            gold_tables.append(d)
    
    if not gold_tables:
        logger.warning("No se encontraron tablas Gold para exportar.")
        return

    for table_name in gold_tables:
        try:
            logger.info(f"Exportando tabla Gold: {table_name}")
            path = os.path.join(GOLD_PATH, table_name)
            dt = DeltaTable(path)
            df = dt.to_pandas()
            
            # Limpieza de columnas técnicas de pandas/delta (como __index_level_0__)
            if '__index_level_0__' in df.columns:
                df = df.drop(columns=['__index_level_0__'])
            
            # Exportación a Postgres
            df.to_sql(
                name=table_name,
                con=engine,
                schema=ANALYTICS_SCHEMA,
                if_exists='replace',
                index=False
            )
            logger.info(f"[{table_name}] Exportación EXITOSA.")
            
        except Exception as e:
            logger.error(f"[{table_name}] Error durante la exportación: {e}")

    logger.info("Finalización exitosa de la exportación a Analytics.")

if __name__ == "__main__":
    export_gold_to_postgres()
