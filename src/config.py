import os

# Delta Lake storage paths
BASE_DATA_PATH = "data"
BRONZE_PATH = os.path.join(BASE_DATA_PATH, "bronze")
SILVER_PATH = os.path.join(BASE_DATA_PATH, "silver")
GOLD_PATH = os.path.join(BASE_DATA_PATH, "gold")

# Database Schemas
RAW_SCHEMA = "raw"
ANALYTICS_SCHEMA = "analytics"

# Tables to process
TABLES = ["brands", "perfumes", "customers", "locations", "sales"]
