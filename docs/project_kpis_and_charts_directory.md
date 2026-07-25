# Master Directory: Project KPIs, Aggregations, & Visual Charts

This document serves as the master catalog of all database metrics, financial KPIs, and data visualizations developed throughout the **Retailmart Cross-Functional BI Dashboard** project.

---

## 1. Phase 4: Exploratory Data Analysis (EDA)
These metrics and charts are focused on understanding baseline sales volumes, distribution parameters, and auditing database outliers.

### A. Key Performance Indicators (KPIs)
| Metric Name | Business Meaning | SQL Logic / Calculation | Python Equivalent |
| :--- | :--- | :--- | :--- |
| **Gross Transaction Count** | Total volume of orders processed. | `COUNT(order_id)` | `orders_df.shape[0]` |
| **Payment Mode Share (%)** | Distribution of orders across Cash, Online, and Financed modes. | `COUNT(o.order_id) / Total * 100` grouped by `payment_mode` | `orders_df['payment_mode'].value_counts(normalize=True)` |
| **Finance Provider Share (%)** | Market share of financing banks. | `COUNT(o.order_id) / Financed Total * 100` grouped by `finance_provider` | `orders_df[orders_df['finance_provider'] != 'Self-Financed']['finance_provider'].value_counts(normalize=True)` |
| **Price Statistical IQR Bounds** | Upper/Lower limits to audit rogue prices. | IQR = Q3 - Q1; Upper = Q3 + 1.5 * IQR | `orders_df['net_amount'].quantile([0.25, 0.75])` |
| **Pearson Correlation Coefficients** | Linear strength and direction of relationship between price, tax, and discount. | `CORR(net_amount, discount_amount)` in SQL | `orders_df[variables].corr()` |

### B. Visualizations & Charts
1. **Sales Amount Distribution (KDE Histogram):** Displays transaction frequencies across different price ranges.
2. **Sales by Payment Mode (Bivariate Box Plot):** Visualizes the spread and median price of cars sold under Cash vs. Online vs. Financed structures.
3. **Monthly Transactions Volume (Timeline Line Chart):** Shows the volume of orders placed month-over-month.
4. **Financial Metrics Correlation Heatmap:** Plots a color-coded grid representing the strength of correlation between financial columns (total price, discounts, taxes, and net amount).
5. **Database Entity Relationship (ER) Map:** Maps primary and foreign keys linking transaction records to location reference and customer profile tables.

---

## 2. Phase 5: Financial KPIs & Ledger Aggregations
These KPIs analyze general ledger accounts to measure operating costs, dealer payouts, and net profit margins.

### A. Key Performance Indicators (KPIs)
| Metric Name | Business Meaning | General Ledger / Calculation | Python Equivalent |
| :--- | :--- | :--- | :--- |
| **Vehicle Sales Revenue** | Total revenue from car sales transactions. | Sum of `net_amount` in orders table. | `orders_df['net_amount'].sum()` |
| **Spares Revenue** | Monthly revenue from vehicle spare parts. | Account Code: `4100` | `ledger_df[ledger_df['account_code'] == '4100-001']['amount'].sum()` |
| **Service Revenue** | Monthly revenue from repair services. | Account Code: `4200` | `ledger_df[ledger_df['account_code'] == '4200-001']['amount'].sum()` |
| **Operating Expenses (OpEx)** | Total business costs. | Sum of Cost Accounts `5000` through `5600` | `ledger_df[ledger_df['account_code'].str[:4].isin(['5000','5100','5200','5300','5400','5500','5600'])]['amount'].sum()` |
| **Net Profit** | Earnings retained after expenses. | `Total Revenue - Total Expenses` | `total_revenue - total_expenses` |
| **Net Profit Margin (%)** | Corporate profitability percentage. | `(Net Profit / Total Revenue) * 100` | `(net_profit / total_revenue) * 100` |
| **Dealer Payout Ratio (%)** | Dealership commission efficiency. | `(Commissions Paid / Showroom Sales) * 100` | `(total_commission / total_revenue) * 100` |

### B. Visualizations & Charts
1. **Showroom Commission Efficiency (Bar Chart):** Ranks dealerships from lowest commission ratio (highly efficient) to highest payout ratio (needs caps).

---

## 3. Phase 6 & 7: Business Insights & Presentation Styling
These metrics link geographic locations and buyer demographics to isolate growth patterns.

### A. Key Performance Indicators (KPIs)
| Metric Name | Business Meaning | Joins Required | Python Equivalent |
| :--- | :--- | :--- | :--- |
| **Regional Sales Volume** | Sales and order counts per region. | `orders` ➔ `dealers` ➔ `cities` ➔ `states` | `.groupby('region')['net_amount'].sum()` |
| **Top 10 Showrooms** | Highest-grossing dealerships. | `orders` ➔ `dealers` | `.groupby('dealer_name')['net_amount'].sum()` |
| **QoQ Revenue Growth (%)** | Quarter-over-quarter growth rate. | LAG window function over quarterly sum. | `.shift(1)` growth calculation |
| **Customer Segment AOV** | Average Order Value per buyer segment. | `orders` ➔ `customers` | `.groupby('customer_segment')['net_amount'].mean()` |

### B. Visualizations & Charts
1. **Executive P&L combo Chart (Bars + Line):** Double Y-axis chart showing Monthly Revenue (vertical bars) and Net Margin (line chart overlay).
2. **Regional Revenue Contribution (Donut Chart):** Cutout circular chart showing sales splits.
3. **Corporate Expense Allocation (Donut Chart):** Slices operational expenses by cost category (Commissions, COGS, salaries, logistics, etc.).
4. **Customer Segment Value (Donut Chart):** Displays revenue shares driven by Budget vs. Mid vs. Premium buyers.

---

## 4. Phase 8: Django Dashboard App Integration Status

The following elements are currently active and rendering in your web control tower at **`http://127.0.0.1:8000/`**:

1. **4 Scorecards:** Gross Revenue, Operating Expenses, Net Profit, Net Profit Margin.
2. **Interactive Combo Chart:** Monthly Revenue vs. Margin (ApexCharts).
3. **Regional Donut Chart:** Revenue split by geographic zone.
4. **Expense Allocation Donut Chart:** Slices of operating costs.
5. **Customer Segment Donut Chart:** Revenue shares by segment.
6. **Top 10 Showrooms Table:** Dealer name, state, orders count, revenue, commissions, and payout ratio.
