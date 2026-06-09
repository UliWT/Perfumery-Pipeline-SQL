import os
import logging
import sys

# Delta Lake storage paths
BASE_DATA_PATH = "data"
BRONZE_PATH = os.path.join(BASE_DATA_PATH, "bronze")
SILVER_PATH = os.path.join(BASE_DATA_PATH, "silver")
GOLD_PATH = os.path.join(BASE_DATA_PATH, "gold")

# Database Schemas
RAW_SCHEMA = "raw"
ANALYTICS_SCHEMA = "analytics"

# Tables to process
TABLES = ["brands", "perfumes", "customers", "locations", "sales", "inventory"]

# Table groups for orchestration and reporting
ENRICHED_TABLES = ["perfumes_enriched", "sales_enriched", "customers_enriched", "inventory_enriched"]
GOLD_METRICS = ["revenue_by_brand", "top_selling_perfumes", "revenue_by_location"]

# Logging Configuration
def setup_logging():
    """Configures the logging system for the pipeline."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(os.path.join(log_dir, "pipeline.log")),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger("perfumeria_pipeline")

logger = setup_logging()
