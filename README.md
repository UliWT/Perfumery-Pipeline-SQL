# 💧 Niche Perfumery Data Pipeline | ETL Medallion Architecture

*(🇪🇸 Versión en español abajo)*

A robust Batch ETL data pipeline simulating a data engineering workflow for a niche perfumery company (brands like Montale, Mancera, Creed, etc.). Built with **Python, Pandas, Delta Lake, and PostgreSQL**, this project implements a full **Medallion Architecture** to guarantee data quality, traceability, and business intelligence readiness.

## 🏗️ Architecture

The pipeline follows the industry-standard **Medallion Architecture**:

1. **🥉 Bronze (Raw)**: Data is ingested directly from the PostgreSQL `raw` schema into local Delta tables. A `processed_at` metadata timestamp is added.
2. **🥈 Silver (Standardized & Cleaned)**: 
   - **Data Quality**: Implementation of business rules (e.g., filtering negative prices, invalid emails, negative stock).
   - **Enrichment**: Joins and merges to create denormalized tables (e.g., `sales_enriched` containing customer, location, and product details).
3. **🥇 Gold (Aggregated)**: Business metrics are calculated (Revenue by Brand, Top Selling Perfumes, Revenue by Location).
4. **📤 Export (Analytics)**: Gold tables are exported back to the PostgreSQL `analytics` schema for consumption by BI tools (Power BI, Tableau, DBeaver).

## 🚀 Features
- **Data Quality**: Custom business rules per entity preventing bad data from flowing downstream.
- **Professional Logging**: Centralized logging system (`logs/pipeline.log`) tracking every ETL step, discarded rows, and errors.
- **Unit Testing**: Comprehensive `pytest` suite ensuring transformation logic and business rules remain intact.
- **CLI Tool**: An interactive Bash script (`using/using_cli.sh`) to run the pipeline, check system health, and explore Delta layers.

## 🛠️ Tech Stack
- **Language**: Python 3.12
- **Data Processing**: Pandas
- **Storage**: Delta Lake (local)
- **Database**: PostgreSQL (SQLAlchemy, Psycopg2)
- **Testing**: Pytest

---

# 💧 Pipeline de Datos Perfumería Nicho | Arquitectura Medallion

*(🇪🇸 Spanish Version)*

Un pipeline de datos Batch ETL robusto que simula el flujo de trabajo de ingeniería de datos para una empresa de perfumería nicho. Construido con **Python, Pandas, Delta Lake y PostgreSQL**, este proyecto implementa una **Arquitectura Medallion** completa para garantizar la calidad de los datos, la trazabilidad y la preparación para Business Intelligence.

## 🏗️ Arquitectura

El pipeline sigue el estándar de la industria **Arquitectura Medallion**:

1. **🥉 Bronze (Crudo)**: Los datos se ingieren directamente desde el esquema `raw` de PostgreSQL a tablas Delta locales. Se agrega un timestamp `processed_at`.
2. **🥈 Silver (Estandarizado y Limpio)**: 
   - **Calidad de Datos (DQ)**: Implementación de reglas de negocio (ej. filtrado de precios negativos, emails inválidos, stock negativo).
   - **Enriquecimiento**: Joins para crear tablas desnormalizadas (ej. `sales_enriched` con detalles de clientes, locaciones y productos).
3. **🥇 Gold (Agregado)**: Cálculo de métricas de negocio (Ingresos por Marca, Perfumes más Vendidos, Ingresos por Locación).
4. **📤 Exportación (Analytics)**: Las tablas Gold se exportan de vuelta al esquema `analytics` de PostgreSQL para su consumo en herramientas de BI.

## 🚀 Características
- **Calidad de Datos**: Reglas de negocio personalizadas por entidad que evitan que datos corruptos avancen en el pipeline.
- **Logging Profesional**: Sistema de logs centralizado (`logs/pipeline.log`) que rastrea cada paso del ETL, filas descartadas y errores.
- **Testing Unitario**: Suite completa de `pytest` que asegura la integridad de la lógica de transformación.
- **Herramienta CLI**: Script interactivo en Bash (`using/using_cli.sh`) para ejecutar el pipeline, revisar la salud del sistema y explorar las capas Delta.

## ⚙️ Cómo Ejecutar / How to Run

1. **Set up the environment**:
    ```bash
    python3 -m venv venvp
    source venvp/bin/activate
    pip install -r requirements.txt
    ```

2. **Configure Database**:
    Create a `.env` file in the root with your Postgres credentials:
    ```ini
    DB_USER=your_user
    DB_PASSWORD=your_password
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=perfumery_db
    ```

3. **Initialize Database**:
    Run the SQL scripts in `sql/` (create tables and seed data).

4. **Run the Pipeline**:
    ```bash
    ./using/using_cli.sh
    # Or directly: python3 main.py
    ```
