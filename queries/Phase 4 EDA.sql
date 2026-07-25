select * from sales_transaction.orders;

SELECT 
    table_name, 
    column_name, 
    data_type,
    is_nullable
FROM information_schema.columns 
WHERE table_schema = 'sales_transaction'
ORDER BY table_name, ordinal_position;


-- 1) Calculate the popularity (volume and percentage share) of each payment method.
SELECT 
    payment_mode,
    COUNT(order_id) AS order_count,
    ROUND((COUNT(order_id)::NUMERIC / (SELECT COUNT(*) FROM sales_transaction.orders) * 100), 2) AS percentage
FROM sales_transaction.orders
GROUP BY payment_mode
ORDER BY order_count DESC;

-- 2)OBJECTIVE: Calculate the market share of each finance provider (bank) for loans/leases.
SELECT 
    finance_provider,
    COUNT(order_id) AS finance_count,
    ROUND((COUNT(order_id)::NUMERIC / (SELECT COUNT(*) FROM sales_transaction.orders WHERE finance_provider IS NOT NULL) * 100), 2) AS partner_share_pct
FROM sales_transaction.orders
WHERE finance_provider IS NOT NULL -- Exclude Cash/EMI purchases that don't use finance partners
GROUP BY finance_provider
ORDER BY finance_count DESC;

-- 3)OBJECTIVE: Calculate the market share of each finance bank using a CTE.
WITH FinanceTotals AS (
    -- Step 1: Pre-calculate the total count of financed orders once
    SELECT COUNT(*) AS total_financed
    FROM sales_transaction.orders
    WHERE finance_provider IS NOT NULL
)
SELECT 
    o.finance_provider,
    COUNT(o.order_id) AS finance_count,
    -- Step 2: Reference our CTE variable 'total_financed' directly
    ROUND((COUNT(o.order_id)::NUMERIC / ft.total_financed * 100), 2) AS partner_share_pct
FROM sales_transaction.orders o
CROSS JOIN FinanceTotals ft -- Link our data rows to the CTE totals
WHERE o.finance_provider IS NOT NULL
GROUP BY o.finance_provider, ft.total_financed
ORDER BY finance_count DESC;


-- OBJECTIVE: Profile the range and spread of sales prices and discounts.
-- This helps us understand our pricing tiers.

SELECT 
    -- 1. Sales Price Profiling
    MIN(net_amount) AS min_net_sale,
    MAX(net_amount) AS max_net_sale,
    ROUND(AVG(net_amount), 2) AS avg_net_sale,
    ROUND(STDDEV(net_amount), 2) AS std_dev_net_sale,
    
    -- 2. Discount Profiling
    MIN(discount_amount) AS min_discount,
    MAX(discount_amount) AS max_discount,
    ROUND(AVG(discount_amount), 2) AS avg_discount
FROM sales_transaction.orders;


-- OBJECTIVE: Compare car transaction sizes across different payment methods.
-- This tells us if financing options increase customer spending.

SELECT 
    payment_mode,
    COUNT(order_id) AS total_orders,
    ROUND(AVG(net_amount), 2) AS average_order_value,
    MIN(net_amount) AS min_order_value,
    MAX(net_amount) AS max_order_value
FROM sales_transaction.orders
GROUP BY payment_mode
ORDER BY average_order_value DESC;

-- OBJECTIVE: Calculate monthly order counts and total revenue chronologically.
-- This helps us spot monthly seasonal growth patterns.

SELECT 
    TO_CHAR(order_date, 'YYYY-MM') AS month,
    COUNT(order_id) AS total_orders,
    SUM(net_amount) AS total_revenue
FROM sales_transaction.orders
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY month ASC; -- Ascending sort to build a proper timeline from past to present


-- OBJECTIVE: Find percentiles, IQR boundaries, and check if we have any pricing outliers.
WITH Stats AS (
    -- Step 1: Calculate Q1, Q3, IQR, and the Outlier Boundaries
    SELECT 
        percentile_cont(0.25) WITHIN GROUP (ORDER BY net_amount) AS q1,
        percentile_cont(0.75) WITHIN GROUP (ORDER BY net_amount) AS q3,
        (percentile_cont(0.75) WITHIN GROUP (ORDER BY net_amount) - 
         percentile_cont(0.25) WITHIN GROUP (ORDER BY net_amount)) AS iqr
    FROM sales_transaction.orders
),
Boundaries AS (
    -- Step 2: Calculate the upper and lower limits using Q1, Q3, and IQR
    SELECT 
        q1,
        q3,
        iqr,
        (q1 - 1.5 * iqr) AS lower_limit,
        (q3 + 1.5 * iqr) AS upper_limit
    FROM Stats
)
-- Step 3: Count how many orders fall outside our statistical limits
SELECT 
    b.q1,
    b.q3,
    b.iqr,
    b.lower_limit,
    b.upper_limit,
    COUNT(o.order_id) AS total_orders,
    -- Count rows that violate the boundaries
    SUM(CASE WHEN o.net_amount > b.upper_limit THEN 1 ELSE 0 END) AS upper_outliers,
    SUM(CASE WHEN o.net_amount < b.lower_limit THEN 1 ELSE 0 END) AS lower_outliers
FROM sales_transaction.orders o
CROSS JOIN Boundaries b
GROUP BY b.q1, b.q3, b.iqr, b.lower_limit, b.upper_limit;