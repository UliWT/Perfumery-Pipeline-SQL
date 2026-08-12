# Perfumery ELT Pipeline

## English

Batch ELT pipeline for a niche perfumery, built with Python, PostgreSQL and SQLAlchemy.

Python coordinates runs, while PostgreSQL performs cleaning, joins, aggregations and quality checks. The production flow does not use Delta Lake, Pandas or local data files.

### Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and configure PostgreSQL credentials. Run the pipeline with `python main.py`, open the viewer with `python main.py view`, and run tests with `python -m pytest -q`.

### Components

- `elt/load_staging.py`: copies `raw` into `staging` with run metadata.
- `sql/elt/02_build_silver.sql`: cleaning and enrichment models.
- `sql/elt/03_build_gold.sql`: business metrics.
- `sql/elt/04_quality_checks.sql`: data quality checks.
- `elt/audit_rejections.py`: rejected-row audit records.
- `elt/console_view.py`: readable Silver and Gold table viewer.
- `audit.pipeline_runs`: execution history.
- `audit.data_quality_issues`: rejected rows and violated rules.

### Docker

```bash
docker compose up --build --abort-on-container-exit --exit-code-from elt
```

Docker initializes the `raw`, `staging` and `audit` schemas through the SQL scripts in `sql/` and `sql/elt/`. PostgreSQL is published on `localhost:5433` for DBeaver. Run the viewer with:

```bash
docker compose up -d db
docker compose run --rm elt python main.py view
```

Data is persisted in the `postgres_data` Docker volume.

## Español

Pipeline ELT batch para una perfumería nicho, construido con Python, PostgreSQL y SQLAlchemy.

Python coordina las ejecuciones y PostgreSQL realiza la limpieza, los joins, las agregaciones y los controles de calidad. El flujo productivo no utiliza Delta Lake, Pandas ni archivos de datos locales.

### Configuración local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copiá `.env.example` como `.env` y configurá las credenciales de PostgreSQL. `.env` está excluido de Git y no debe versionarse. Ejecutá el pipeline con `python main.py`, abrí el visor con `python main.py view` y ejecutá las pruebas con `python -m pytest -q`.

### Componentes

- `elt/load_staging.py`: copia `raw` a `staging` con metadatos de ejecución.
- `sql/elt/02_build_silver.sql`: modelos de limpieza y enriquecimiento.
- `sql/elt/03_build_gold.sql`: métricas de negocio.
- `sql/elt/04_quality_checks.sql`: controles de calidad.
- `elt/audit_rejections.py`: auditoría de filas rechazadas.
- `elt/console_view.py`: visor de tablas Silver y Gold.
- `audit.pipeline_runs`: historial de ejecuciones.
- `audit.data_quality_issues`: filas rechazadas y reglas incumplidas.

### Docker

```bash
docker compose up --build --abort-on-container-exit --exit-code-from elt
```

Docker inicializa los esquemas `raw`, `staging` y `audit` mediante los scripts SQL de `sql/` y `sql/elt/`. PostgreSQL queda publicado en `localhost:5433` para DBeaver. Ejecutá el visor con:

```bash
docker compose up -d db
docker compose run --rm elt python main.py view
```

Los datos quedan persistidos en el volumen Docker `postgres_data`.

