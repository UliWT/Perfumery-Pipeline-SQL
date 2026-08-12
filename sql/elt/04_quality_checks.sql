
SELECT
    'silver_perfumes_positive_price' AS check_name,
    COUNT(*) = 0 AS passed,
    COUNT(*) AS invalid_rows
FROM analytics.silver_perfumes
WHERE price <= 0 OR price IS NULL;

SELECT
    'silver_customers_valid_email' AS check_name,
    COUNT(*) = 0 AS passed,
    COUNT(*) AS invalid_rows
FROM analytics.silver_customers
WHERE email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}$';

SELECT
    'silver_sales_positive_quantity' AS check_name,
    COUNT(*) = 0 AS passed,
    COUNT(*) AS invalid_rows
FROM analytics.silver_sales
WHERE quantity <= 0 OR quantity IS NULL;

SELECT
    'silver_inventory_non_negative_stock' AS check_name,
    COUNT(*) = 0 AS passed,
    COUNT(*) AS invalid_rows
FROM analytics.silver_inventory
WHERE current_stock < 0 OR current_stock IS NULL;

SELECT
    'gold_revenue_not_negative' AS check_name,
    COUNT(*) = 0 AS passed,
    COUNT(*) AS invalid_rows
FROM analytics.gold_revenue_by_brand
WHERE total_revenue < 0 OR total_revenue IS NULL;

