-- ==============================================================================
-- PHARMACY SALES & INVENTORY ANALYTICS - 15 KEY QUERIES
-- Optimized for SQLite & PostgreSQL (with comments explaining syntax adjustments)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Top 10 Products by Revenue
-- ------------------------------------------------------------------------------
-- Identifies the top revenue-generating products, their sales volume and margins.
SELECT 
    product_name, 
    SUM(sales_amount) AS total_revenue,
    COUNT(*) AS transaction_count,
    AVG(profit_margin) AS avg_profit_margin
FROM transactions
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 10;


-- ------------------------------------------------------------------------------
-- QUERY 2: Top 10 Categories by Revenue
-- ------------------------------------------------------------------------------
-- Aggregates sales at the category level and calculates variety & order size.
SELECT 
    category,
    SUM(sales_amount) AS category_revenue,
    COUNT(DISTINCT product_name) AS product_count,
    AVG(sales_amount) AS avg_order_value
FROM transactions
GROUP BY category
ORDER BY category_revenue DESC
LIMIT 10;


-- ------------------------------------------------------------------------------
-- QUERY 3: Monthly Sales Trend (Last 12 Months)
-- ------------------------------------------------------------------------------
-- Tracks monthly performance.
-- SQLite syntax: STRFTIME('%Y-%m', transaction_date)
-- PostgreSQL equivalent: TO_CHAR(transaction_date, 'YYYY-MM')
SELECT 
    STRFTIME('%Y-%m', transaction_date) AS month,
    SUM(sales_amount) AS monthly_revenue,
    COUNT(*) AS transaction_count,
    AVG(sales_amount) AS avg_transaction_value
FROM transactions
GROUP BY STRFTIME('%Y-%m', transaction_date)
ORDER BY month DESC
LIMIT 12;


-- ------------------------------------------------------------------------------
-- QUERY 4: Revenue by Category
-- ------------------------------------------------------------------------------
-- Calculates market share (percentage of total revenue) for each product category.
SELECT 
    category,
    SUM(sales_amount) AS revenue,
    ROUND(SUM(sales_amount) * 100.0 / (SELECT SUM(sales_amount) FROM transactions), 2) AS revenue_percentage,
    COUNT(*) AS orders
FROM transactions
GROUP BY category
ORDER BY revenue DESC;


-- ------------------------------------------------------------------------------
-- QUERY 5: Revenue by Region/Store
-- ------------------------------------------------------------------------------
-- Compares sales performance, customer base, and transaction values across locations.
SELECT 
    store_location,
    SUM(sales_amount) AS store_revenue,
    COUNT(DISTINCT customer_id) AS unique_customers,
    AVG(sales_amount) AS avg_transaction
FROM transactions
GROUP BY store_location
ORDER BY store_revenue DESC;


-- ------------------------------------------------------------------------------
-- QUERY 6: Best Performing Store (Multi-Metrics)
-- ------------------------------------------------------------------------------
-- Uses window functions to rank stores by revenue, evaluating multi-metric health.
SELECT 
    store_location,
    SUM(sales_amount) AS total_revenue,
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT customer_id) AS unique_customers,
    AVG(profit_margin) AS avg_profit_margin,
    RANK() OVER (ORDER BY SUM(sales_amount) DESC) AS revenue_rank
FROM transactions
GROUP BY store_location
ORDER BY total_revenue DESC;


-- ------------------------------------------------------------------------------
-- QUERY 7: Low Stock Products Alert
-- ------------------------------------------------------------------------------
-- Identifies products near stockout, categorizing urgency and days remaining.
SELECT 
    product_name,
    category,
    current_stock,
    reorder_level,
    CASE 
        WHEN current_stock < reorder_level THEN 'URGENT'
        WHEN current_stock < reorder_level * 1.5 THEN 'WARNING'
        ELSE 'OK'
    END AS stock_status,
    CASE 
        WHEN current_stock = 0 THEN 0
        ELSE CAST(current_stock AS FLOAT) / avg_daily_sales
    END AS days_to_stockout
FROM inventory i
JOIN products p ON i.product_id = p.product_id
WHERE current_stock <= reorder_level * 2
ORDER BY current_stock ASC;


-- ------------------------------------------------------------------------------
-- QUERY 8: High Profit Products
-- ------------------------------------------------------------------------------
-- Filters products whose profit margins exceed the company-wide average.
SELECT 
    product_name,
    category,
    SUM(sales_amount) AS total_revenue,
    SUM(profit) AS total_profit,
    AVG(profit_margin) AS avg_profit_margin,
    SUM(quantity) AS units_sold
FROM transactions
GROUP BY product_name, category
HAVING AVG(profit_margin) > (SELECT AVG(profit_margin) FROM transactions)
ORDER BY total_profit DESC
LIMIT 10;


-- ------------------------------------------------------------------------------
-- QUERY 9: Slow Moving Products (High Stock, Low Sales)
-- ------------------------------------------------------------------------------
-- Flags products with excessive stock and very low sales volume over the last 30 days.
-- SQLite syntax: DATE('now', '-30 days')
-- PostgreSQL equivalent: CURRENT_DATE - INTERVAL '30 days'
SELECT 
    p.product_name,
    p.category,
    i.current_stock,
    COUNT(t.transaction_id) AS sales_count_last_30days,
    ROUND(i.current_stock / NULLIF(COUNT(t.transaction_id), 0.0), 2) AS days_supply,
    i.cost_price,
    i.current_stock * i.cost_price AS inventory_value_at_risk
FROM inventory i
JOIN products p ON i.product_id = p.product_id
LEFT JOIN transactions t ON i.product_id = t.product_id 
    AND t.transaction_date >= DATE('2026-03-31', '-30 days') -- Anchored to dataset end date (2026-03-31)
GROUP BY p.product_name, p.category, i.current_stock, i.cost_price
HAVING COUNT(t.transaction_id) < 5 AND i.current_stock > 100
ORDER BY days_supply DESC;


-- ------------------------------------------------------------------------------
-- QUERY 10: Product Demand Ranking
-- ------------------------------------------------------------------------------
-- Ranks products by transaction frequency, showing demand concentration.
SELECT 
    RANK() OVER (ORDER BY COUNT(*) DESC) AS demand_rank,
    product_name,
    category,
    COUNT(*) AS purchase_frequency,
    SUM(sales_amount) AS total_revenue,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions), 2) AS demand_percentage
FROM transactions
GROUP BY product_name, category
ORDER BY demand_rank;


-- ------------------------------------------------------------------------------
-- QUERY 11: Customer Segmentation (RFM Analysis)
-- ------------------------------------------------------------------------------
-- Segments customers using NTILE to ensure dual compatibility (SQLite & PostgreSQL)
-- NTILE(4) partitions customers into 4 equal quarters by total purchase value.
WITH customer_rfm AS (
    SELECT 
        t.customer_id,
        c.customer_name,
        MAX(t.transaction_date) AS last_purchase_date,
        COUNT(DISTINCT DATE(t.transaction_date)) AS purchase_frequency,
        SUM(t.sales_amount) AS customer_lifetime_value,
        NTILE(4) OVER (ORDER BY SUM(t.sales_amount)) AS clv_quartile
    FROM transactions t
    JOIN customers c ON t.customer_id = c.customer_id
    GROUP BY t.customer_id, c.customer_name
)
SELECT 
    customer_id,
    customer_name,
    last_purchase_date,
    purchase_frequency,
    customer_lifetime_value,
    CASE 
        WHEN clv_quartile = 4 THEN 'VIP'
        WHEN clv_quartile = 1 THEN 'At-Risk'
        ELSE 'Regular'
    END AS customer_segment
FROM customer_rfm
ORDER BY customer_lifetime_value DESC;


-- ------------------------------------------------------------------------------
-- QUERY 12: Inventory Turnover by Category
-- ------------------------------------------------------------------------------
-- Measures efficiency of inventory by comparing annual sales to current stock value.
SELECT 
    p.category,
    SUM(i.current_stock * p.cost_price) AS avg_inventory_value,
    SUM(t.sales_amount) AS annual_sales,
    ROUND(SUM(t.sales_amount) / NULLIF(SUM(i.current_stock * p.cost_price), 0.0), 2) AS inventory_turnover_ratio,
    CASE 
        WHEN ROUND(SUM(t.sales_amount) / NULLIF(SUM(i.current_stock * p.cost_price), 0.0), 2) > 4 THEN 'Fast Moving'
        WHEN ROUND(SUM(t.sales_amount) / NULLIF(SUM(i.current_stock * p.cost_price), 0.0), 2) > 2 THEN 'Normal'
        ELSE 'Slow Moving'
    END AS movement_status
FROM inventory i
JOIN products p ON i.product_id = p.product_id
LEFT JOIN transactions t ON p.product_id = t.product_id
GROUP BY p.category
ORDER BY inventory_turnover_ratio DESC;


-- ------------------------------------------------------------------------------
-- QUERY 13: Sales Performance by Day of Week
-- ------------------------------------------------------------------------------
-- Analyzes sales patterns by weekday.
-- SQLite syntax: STRFTIME('%w', transaction_date) where 0=Sunday, 6=Saturday
-- PostgreSQL equivalent: EXTRACT(DOW FROM transaction_date)
SELECT 
    CASE CAST(STRFTIME('%w', transaction_date) AS INTEGER)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS day_of_week,
    COUNT(*) AS transaction_count,
    SUM(sales_amount) AS daily_revenue,
    AVG(sales_amount) AS avg_transaction_value,
    MAX(sales_amount) AS max_transaction
FROM transactions
GROUP BY STRFTIME('%w', transaction_date)
ORDER BY CAST(STRFTIME('%w', transaction_date) AS INTEGER);


-- ------------------------------------------------------------------------------
-- QUERY 14: Category Performance Dashboard (Multi-Metric)
-- ------------------------------------------------------------------------------
-- Comprehensive performance health evaluation across all categories.
SELECT 
    category,
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(sales_amount) AS total_revenue,
    SUM(profit) AS total_profit,
    ROUND(AVG(profit_margin), 2) AS avg_profit_margin,
    COUNT(DISTINCT product_name) AS product_count,
    MIN(sales_amount) AS min_transaction,
    MAX(sales_amount) AS max_transaction
FROM transactions
GROUP BY category
ORDER BY total_revenue DESC;


-- ------------------------------------------------------------------------------
-- QUERY 15: Year-over-Year Comparison
-- ------------------------------------------------------------------------------
-- Tracks year-over-year monthly performance using the LAG window function.
-- SQLite syntax: STRFTIME('%m', ...)
SELECT 
    STRFTIME('%m', transaction_date) AS month,
    STRFTIME('%Y', transaction_date) AS year,
    SUM(sales_amount) AS monthly_revenue,
    COUNT(*) AS transaction_count,
    LAG(SUM(sales_amount)) OVER (PARTITION BY STRFTIME('%m', transaction_date) ORDER BY STRFTIME('%Y', transaction_date)) AS previous_year_revenue,
    ROUND(((SUM(sales_amount) - LAG(SUM(sales_amount)) OVER (PARTITION BY STRFTIME('%m', transaction_date) ORDER BY STRFTIME('%Y', transaction_date))) / 
           NULLIF(LAG(SUM(sales_amount)) OVER (PARTITION BY STRFTIME('%m', transaction_date) ORDER BY STRFTIME('%Y', transaction_date)), 0.0) * 100), 2) AS yoy_growth_percentage
FROM transactions
GROUP BY STRFTIME('%Y-%m', transaction_date)
ORDER BY year DESC, month;
