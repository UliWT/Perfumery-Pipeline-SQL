# Perfumeria Nicho Data Pipeline

A Medallion architecture data pipeline for processing niche perfumery data (Montale, Mancera, etc.) using Python, Pandas, Delta Lake, and PostgreSQL.

## Architecture

The pipeline follows the **Medallion Architecture**:

1.  **Bronze (Raw)**: Data is ingested directly from the PostgreSQL `raw` schema into Delta tables. A `processed_at` timestamp is added.
2.  **Silver (Standardized)**: Data is cleaned, standardized (snake_case, type casting), and enriched (e.g., joining perfumes with brands).
3.  **Gold (Aggregated)**: Business metrics are calculated, such as revenue by brand, top-selling perfumes, and revenue by location.
4.  **Export**: Gold tables are exported back to the PostgreSQL `analytics` schema for consumption by BI tools (e.g., DBeaver, Power BI).

## Tech Stack

- **Language**: Python 3.12
- **Data Processing**: Pandas
- **Storage**: Delta Lake (local)
- **Database**: PostgreSQL
- **ORM/Connection**: SQLAlchemy, Psycopg2

## Project Structure

```text
Perfumeria/
├── main.py                 # Pipeline orchestrator
├── extract/
│   └── ingest_to_bronze.py # Postgres -> Bronze
├── transform/
│   ├── silver_transformation.py # Bronze -> Silver
│   └── gold_aggregation.py      # Silver -> Gold
├── load/
│   └── export_to_postgres.py    # Gold -> Postgres Analytics
├── src/
│   └── config.py           # Configuration (paths, schemas)
├── sql/
│   ├── connection.py       # DB connection manager
│   ├── init_db.sql         # DB and schema initialization
│   └── seed_data.sql       # Initial raw data
└── data/                   # Delta Lake storage (Bronze/Silver/Gold)
```

## How to Run

1.  **Set up the environment**:
    ```bash
    python3 -m venv venvp
    source venvp/bin/activate
    pip install pandas sqlalchemy deltalake psycopg2-binary python-dotenv
    ```

2.  **Configure Database**:
    Create a `.env` file in the root with your Postgres credentials:
    ```ini
    DB_USER=your_user
    DB_PASSWORD=your_password
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=perfumeria_db
    ```

3.  **Initialize Database**:
    Run the SQL scripts in `sql/` to create schemas and tables and seed the data.

4.  **Run the Pipeline**:
    ```bash
    python3 main.py
    ```

## Verification

After running the pipeline, you can check the results in the `analytics` schema of your PostgreSQL database using DBeaver or any other SQL client.
