-- ====================================================================
-- PHASE 6: BUSINESS INSIGHTS & AGGREGATIONS
-- ====================================================================

-- --------------------------------------------------------------------
-- CHALLENGE 1: Regional Sales Performance
-- Goal: Identify which geographical zones contribute the most to sales.
-- --------------------------------------------------------------------
SELECT 
    s.region,
    COUNT(o.order_id) AS total_orders,
    SUM(o.net_amount) AS total_revenue
FROM sales_transaction.orders o
JOIN dealer.dealers d ON o.dealer_id = d.dealer_id
JOIN location_reference.cities c ON d.city_id = c.city_id
JOIN location_reference.states s ON c.state_id = s.state_id
GROUP BY s.region
ORDER BY total_revenue DESC;


-- --------------------------------------------------------------------
-- CHALLENGE 2: Top 10 Showroom Leaderboard
-- Goal: Identify our top 10 showrooms by revenue and their state.
-- --------------------------------------------------------------------
SELECT 
    d.dealer_name,
    s.state_name,
    COUNT(o.order_id) AS total_orders,
    SUM(o.net_amount) AS total_revenue
FROM sales_transaction.orders o
JOIN dealer.dealers d ON o.dealer_id = d.dealer_id
JOIN location_reference.cities c ON d.city_id = c.city_id
JOIN location_reference.states s ON c.state_id = s.state_id
GROUP BY d.dealer_name, s.state_name
ORDER BY total_revenue DESC
LIMIT 10;


-- --------------------------------------------------------------------
-- CHALLENGE 3: Seasonal Quarterly Growth Rate
-- Goal: Calculate QoQ growth percentages using the LAG() window function.
-- --------------------------------------------------------------------
WITH QuarterlySales AS (
    SELECT 
        TO_CHAR(order_date, 'YYYY-"Q"Q') AS quarter,
        SUM(net_amount) AS current_revenue
    FROM sales_transaction.orders
    GROUP BY TO_CHAR(order_date, 'YYYY-"Q"Q')
)
SELECT 
    quarter,
    current_revenue,
    LAG(current_revenue) OVER (ORDER BY quarter) AS previous_revenue,
    ROUND(
        ((current_revenue - LAG(current_revenue) OVER (ORDER BY quarter)) / 
         LAG(current_revenue) OVER (ORDER BY quarter) * 100)
    , 2) AS qoq_growth_pct
FROM QuarterlySales
ORDER BY quarter ASC;


-- --------------------------------------------------------------------
-- CHALLENGE 4: Customer Segment Profitability
-- Goal: Identify the sales contribution and AOV across buyer categories.
-- --------------------------------------------------------------------
SELECT 
    c.customer_segment,
    COUNT(o.order_id) AS total_orders,
    SUM(o.net_amount) AS total_revenue,
    ROUND(AVG(o.net_amount), 2) AS average_order_value
FROM sales_transaction.orders o
JOIN customer.customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_segment
ORDER BY total_revenue DESC;
