-- Gold models: business-facing aggregates built from Silver.

CREATE SCHEMA IF NOT EXISTS analytics;

DROP TABLE IF EXISTS analytics.gold_revenue_by_brand;
DROP TABLE IF EXISTS analytics.gold_top_selling_perfumes;
DROP TABLE IF EXISTS analytics.gold_revenue_by_location;

CREATE TABLE analytics.gold_revenue_by_brand AS
SELECT
    brand_name,
    SUM(quantity * price) AS total_revenue
FROM analytics.silver_sales_enriched
GROUP BY brand_name
ORDER BY total_revenue DESC;

CREATE TABLE analytics.gold_top_selling_perfumes AS
SELECT
    perfume_name,
    SUM(quantity) AS total_quantity
FROM analytics.silver_sales_enriched
GROUP BY perfume_name
ORDER BY total_quantity DESC;

CREATE TABLE analytics.gold_revenue_by_location AS
SELECT
    location_name,
    SUM(quantity * price) AS total_revenue
FROM analytics.silver_sales_enriched
GROUP BY location_name
ORDER BY total_revenue DESC;

