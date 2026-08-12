-- Staging keeps a database copy of the source rows plus ingestion metadata.
-- The source columns remain unchanged so that transformations happen later.

CREATE TABLE IF NOT EXISTS staging.brands (
    LIKE raw.brands INCLUDING DEFAULTS INCLUDING CONSTRAINTS
);
ALTER TABLE staging.brands
    ADD COLUMN IF NOT EXISTS _ingested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN IF NOT EXISTS _run_id UUID;

CREATE TABLE IF NOT EXISTS staging.perfumes (
    LIKE raw.perfumes INCLUDING DEFAULTS INCLUDING CONSTRAINTS
);
ALTER TABLE staging.perfumes
    ADD COLUMN IF NOT EXISTS _ingested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN IF NOT EXISTS _run_id UUID;

CREATE TABLE IF NOT EXISTS staging.customers (
    LIKE raw.customers INCLUDING DEFAULTS INCLUDING CONSTRAINTS
);
ALTER TABLE staging.customers
    ADD COLUMN IF NOT EXISTS _ingested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN IF NOT EXISTS _run_id UUID;

CREATE TABLE IF NOT EXISTS staging.locations (
    LIKE raw.locations INCLUDING DEFAULTS INCLUDING CONSTRAINTS
);
ALTER TABLE staging.locations
    ADD COLUMN IF NOT EXISTS _ingested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN IF NOT EXISTS _run_id UUID;

CREATE TABLE IF NOT EXISTS staging.sales (
    LIKE raw.sales INCLUDING DEFAULTS INCLUDING CONSTRAINTS
);
ALTER TABLE staging.sales
    ADD COLUMN IF NOT EXISTS _ingested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN IF NOT EXISTS _run_id UUID;

CREATE TABLE IF NOT EXISTS staging.inventory (
    LIKE raw.inventory INCLUDING DEFAULTS INCLUDING CONSTRAINTS
);
ALTER TABLE staging.inventory
    ADD COLUMN IF NOT EXISTS _ingested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN IF NOT EXISTS _run_id UUID;

CREATE TABLE IF NOT EXISTS audit.pipeline_runs (
    run_id UUID PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    finished_at TIMESTAMPTZ,
    status TEXT NOT NULL CHECK (status IN ('running', 'success', 'failed')),
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS audit.data_quality_issues (
    issue_id BIGSERIAL PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES audit.pipeline_runs(run_id),
    entity TEXT NOT NULL,
    source_id TEXT,
    rule_name TEXT NOT NULL,
    details TEXT,
    detected_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
