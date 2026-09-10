-- OBJECTIVE: Calculate the total net revenue from vehicle sales for each month.
SELECT 
    TO_CHAR(order_date, 'YYYY-MM') AS month,
    SUM(net_amount) AS vehicle_revenue
FROM sales_transaction.orders
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY month ASC;

-- OBJECTIVE: Join the general ledger and account lookup tables, 
-- and calculate the monthly sums of all company expenses.

SELECT 
    TO_CHAR(le.transaction_date, 'YYYY-MM') AS month,
    SUBSTRING(gl.account_code FROM 1 FOR 4) AS category_code,
    SUM(le.debit_amount) AS total_expense
FROM finance_accounting.ledger_entries le
JOIN finance_accounting.gl_accounts gl ON le.account_id = gl.account_id
WHERE gl.account_type = 'Expense' -- Filter for expenses only
GROUP BY 
    TO_CHAR(le.transaction_date, 'YYYY-MM'),
    SUBSTRING(gl.account_code FROM 1 FOR 4)
ORDER BY month ASC, category_code ASC;


-- OBJECTIVE: Join orders, dealers, and commissions to calculate total sales 
-- and payout efficiency percentages for each showroom.
-- Uses pre-aggregated CTEs to avoid Many-to-Many row duplication.

WITH OrderAgg AS (
    SELECT 
        dealer_id,
        COUNT(order_id) AS total_orders,
        SUM(net_amount) AS total_revenue
    FROM sales_transaction.orders
    GROUP BY dealer_id
),
CommAgg AS (
    SELECT 
        dealer_id,
        SUM(total_commission) AS total_commission
    FROM dealer_network.dealer_commissions
    GROUP BY dealer_id
)
SELECT 
    d.dealer_name,
    COALESCE(o.total_orders, 0) AS total_orders,
    COALESCE(o.total_revenue, 0) AS total_revenue,
    COALESCE(c.total_commission, 0) AS total_commission,
    -- Calculate what % of sales revenue goes back to the dealer as commission
    ROUND((COALESCE(c.total_commission, 0) / NULLIF(o.total_revenue, 0) * 100), 2) AS payout_ratio_pct
FROM dealer.dealers d
LEFT JOIN OrderAgg o ON d.dealer_id = o.dealer_id
LEFT JOIN CommAgg c ON d.dealer_id = c.dealer_id
ORDER BY total_revenue DESC;


-- OBJECTIVE: Build a complete monthly Profit & Loss (P&L) statement.
-- We use 3 separate CTEs to fetch Vehicle Revenue, Other Revenue, and Expenses,
-- then join them together to run the margin math.

WITH VehicleRevenue AS (
    -- CTE 1: Get monthly vehicle sales
    SELECT 
        TO_CHAR(order_date, 'YYYY-MM') AS month,
        SUM(net_amount) AS vehicle_rev
    FROM sales_transaction.orders
    GROUP BY TO_CHAR(order_date, 'YYYY-MM')
),
OtherIncome AS (
    -- CTE 2: Get monthly spares and service income
    SELECT 
        TO_CHAR(le.transaction_date, 'YYYY-MM') AS month,
        SUM(CASE WHEN gl.account_code LIKE '4100%' THEN le.credit_amount ELSE 0 END) AS spares_rev,
        SUM(CASE WHEN gl.account_code LIKE '4200%' THEN le.credit_amount ELSE 0 END) AS service_rev
    FROM finance_accounting.ledger_entries le
    JOIN finance_accounting.gl_accounts gl ON le.account_id = gl.account_id
    WHERE gl.account_type = 'Income'
    GROUP BY TO_CHAR(le.transaction_date, 'YYYY-MM')
),
Expenses AS (
    -- CTE 3: Get monthly operating expenses
    SELECT 
        TO_CHAR(le.transaction_date, 'YYYY-MM') AS month,
        SUM(CASE WHEN gl.account_code LIKE '5000%' THEN le.debit_amount ELSE 0 END) AS cogs,
        SUM(CASE WHEN gl.account_code LIKE '5100%' THEN le.debit_amount ELSE 0 END) AS manufacturing,
        SUM(CASE WHEN gl.account_code LIKE '5200%' THEN le.debit_amount ELSE 0 END) AS salaries,
        SUM(CASE WHEN gl.account_code LIKE '5300%' THEN le.debit_amount ELSE 0 END) AS marketing,
        SUM(CASE WHEN gl.account_code LIKE '5400%' THEN le.debit_amount ELSE 0 END) AS logistics,
        SUM(CASE WHEN gl.account_code LIKE '5500%' THEN le.debit_amount ELSE 0 END) AS commissions,
        SUM(CASE WHEN gl.account_code LIKE '5600%' THEN le.debit_amount ELSE 0 END) AS admin
    FROM finance_accounting.ledger_entries le
    JOIN finance_accounting.gl_accounts gl ON le.account_id = gl.account_id
    WHERE gl.account_type = 'Expense'
    GROUP BY TO_CHAR(le.transaction_date, 'YYYY-MM')
)
-- Main Select: Join all 3 CTEs and calculate P&L KPIs
SELECT 
    vr.month,
    -- Total Revenue = Vehicle Sales + Spares Sales + Service Sales
    (vr.vehicle_rev + COALESCE(oi.spares_rev, 0) + COALESCE(oi.service_rev, 0)) AS total_revenue,
    
    -- Total Expenses = Sum of all 7 cost categories
    (COALESCE(e.cogs, 0) + COALESCE(e.manufacturing, 0) + COALESCE(e.salaries, 0) + 
     COALESCE(e.marketing, 0) + COALESCE(e.logistics, 0) + COALESCE(e.commissions, 0) + 
     COALESCE(e.admin, 0)) AS total_expenses,
     
    -- Gross Profit = Total Revenue - COGS
    (vr.vehicle_rev + COALESCE(oi.spares_rev, 0) + COALESCE(oi.service_rev, 0)) - COALESCE(e.cogs, 0) AS gross_profit,
    
    -- Net Profit = Total Revenue - Total Expenses
    (vr.vehicle_rev + COALESCE(oi.spares_rev, 0) + COALESCE(oi.service_rev, 0)) - 
    (COALESCE(e.cogs, 0) + COALESCE(e.manufacturing, 0) + COALESCE(e.salaries, 0) + 
     COALESCE(e.marketing, 0) + COALESCE(e.logistics, 0) + COALESCE(e.commissions, 0) + 
     COALESCE(e.admin, 0)) AS net_profit,
     
    -- Margin = (Net Profit / Total Revenue) * 100
    ROUND(
        ((vr.vehicle_rev + COALESCE(oi.spares_rev, 0) + COALESCE(oi.service_rev, 0)) - 
         (COALESCE(e.cogs, 0) + COALESCE(e.manufacturing, 0) + COALESCE(e.salaries, 0) + 
          COALESCE(e.marketing, 0) + COALESCE(e.logistics, 0) + COALESCE(e.commissions, 0) + 
          COALESCE(e.admin, 0))) / 
        (vr.vehicle_rev + COALESCE(oi.spares_rev, 0) + COALESCE(oi.service_rev, 0)) * 100
    , 2) AS net_profit_margin_pct
FROM VehicleRevenue vr
LEFT JOIN OtherIncome oi ON vr.month = oi.month
LEFT JOIN Expenses e ON vr.month = e.month
ORDER BY vr.month ASC;


