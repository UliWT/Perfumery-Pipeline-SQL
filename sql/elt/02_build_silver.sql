-- Silver models: clean and standardize data inside PostgreSQL.
-- These tables intentionally contain no source ingestion metadata.

CREATE SCHEMA IF NOT EXISTS analytics;

DROP TABLE IF EXISTS analytics.silver_sales_enriched;
DROP TABLE IF EXISTS analytics.silver_inventory_enriched;
DROP TABLE IF EXISTS analytics.silver_customers_enriched;
DROP TABLE IF EXISTS analytics.silver_perfumes_enriched;
DROP TABLE IF EXISTS analytics.silver_inventory;
DROP TABLE IF EXISTS analytics.silver_sales;
DROP TABLE IF EXISTS analytics.silver_customers;
DROP TABLE IF EXISTS analytics.silver_locations;
DROP TABLE IF EXISTS analytics.silver_perfumes;
DROP TABLE IF EXISTS analytics.silver_brands;

-- Base entities: DISTINCT replaces the old exact duplicate removal.
CREATE TABLE analytics.silver_brands AS
SELECT DISTINCT
    id,
    btrim(name) AS name,
    NULLIF(btrim(country), '') AS country
FROM staging.brands;

CREATE TABLE analytics.silver_perfumes AS
SELECT DISTINCT
    id,
    brand_id,
    btrim(name) AS name,
    NULLIF(btrim(perfume_type), '') AS perfume_type,
    size_ml,
    price
FROM staging.perfumes
WHERE price > 0
  AND name IS NOT NULL
  AND btrim(name) <> '';

CREATE TABLE analytics.silver_locations AS
SELECT DISTINCT
    id,
    NULLIF(btrim(name), '') AS name,
    NULLIF(btrim(state), '') AS state
FROM staging.locations;

CREATE TABLE analytics.silver_customers AS
SELECT DISTINCT
    id,
    btrim(first_name) AS first_name,
    btrim(last_name) AS last_name,
    btrim(email) AS email,
    location AS location_id
FROM staging.customers
WHERE email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}$';

CREATE TABLE analytics.silver_sales AS
SELECT DISTINCT
    id,
    customer_id,
    perfume_id,
    location_id,
    quantity,
    sale_date
FROM staging.sales
WHERE quantity > 0
  AND customer_id IS NOT NULL
  AND perfume_id IS NOT NULL
  AND location_id IS NOT NULL;

CREATE TABLE analytics.silver_inventory AS
SELECT DISTINCT
    id,
    perfume_id,
    current_stock,
    last_updated
FROM staging.inventory
WHERE current_stock >= 0;

-- Enriched models: joins executed by PostgreSQL.
CREATE TABLE analytics.silver_perfumes_enriched AS
SELECT
    b.name AS brand_name,
    p.name,
    p.perfume_type,
    p.size_ml,
    p.price,
    b.country
FROM analytics.silver_perfumes p
JOIN analytics.silver_brands b ON b.id = p.brand_id;

CREATE TABLE analytics.silver_sales_enriched AS
SELECT
    s.sale_date,
    c.first_name,
    c.last_name,
    l.name AS location_name,
    l.state,
    b.name AS brand_name,
    p.name AS perfume_name,
    s.quantity,
    p.price
FROM analytics.silver_sales s
LEFT JOIN analytics.silver_customers c ON c.id = s.customer_id
LEFT JOIN analytics.silver_locations l ON l.id = s.location_id
LEFT JOIN analytics.silver_perfumes p ON p.id = s.perfume_id
LEFT JOIN analytics.silver_brands b ON b.id = p.brand_id;

CREATE TABLE analytics.silver_customers_enriched AS
SELECT
    c.first_name,
    c.last_name,
    c.email,
    l.name AS location_name,
    l.state
FROM analytics.silver_customers c
JOIN analytics.silver_locations l ON l.id = c.location_id;

CREATE TABLE analytics.silver_inventory_enriched AS
SELECT
    b.name AS brand_name,
    p.name AS perfume_name,
    i.current_stock
FROM analytics.silver_inventory i
LEFT JOIN analytics.silver_perfumes p ON p.id = i.perfume_id
LEFT JOIN analytics.silver_brands b ON b.id = p.brand_id;

