-- Schemas used by the ELT pipeline.
-- raw is the source schema and is intentionally not modified here.
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;

