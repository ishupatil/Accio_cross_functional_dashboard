# Master Guide: Executive Operations & Financial Dashboard

This master document contains the step-by-step setup guide to run the project with your live pgAdmin PostgreSQL database, page-by-page operational explanations, full KPI definitions, and data-driven strategic insights.

---

## 🚀 Part 1: How to Setup and Run the Project

Follow these steps to configure your database and launch the server on your computer:

### 1. Open Terminal & Navigate to the Project Root
Open your terminal application (e.g., **PowerShell** or **Command Prompt**) and move into the workspace directory:
```bash
cd "e:\SQL ACCIO JOB\Cross functional dashboard"
```

### 2. Configure Database Credentials (.env)
Ensure your database credentials inside the **`.env`** file match your local pgAdmin PostgreSQL setup:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=test
DB_USER=postgres
DB_PASSWORD=your_secure_password_here
DB_SCHEMA=public
```

### 3. Install Required Dependencies
Activate your Python environment and run the package installer:
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
Create Django's core authentication and session tables in the PostgreSQL database's `public` schema:
```bash
python manage.py migrate
```

### 5. Seed the Administrative User
Create the default superuser account inside your live PostgreSQL database to authenticate logins:
```bash
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
```
*Note: If the `admin` user is already registered, this script will notify you. You can update password hashes via `u.set_password('admin123'); u.save()`.*

### 6. Launch the Server
Start the development server:
```bash
python manage.py runserver
```
*Note: Keep this terminal window open. To stop the server at any point, press `Ctrl + C`.*

### 7. Access the Dashboard in your Web Browser
Open your browser and navigate to: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**
* **Username:** `admin`
* **Password:** `admin123`

### 🔑 How to Change User Credentials
If you want to edit an existing user's name or password, choose one of these methods:

#### Method A: Via the Django Admin Panel (Visual Interface)
1. Go to: **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)** and log in.
2. Click **Users**, select the user (e.g. `admin`).
3. To change the username: Modify the **Username** field.
4. To change the password: Click **"change the password using this form"**, enter the new password, and click **Save**.

#### Method B: Via the Python Terminal Shell (Programmatic)
1. Run: `python manage.py shell`
2. Run this script in the shell (replace `'admin'` with current username):
   ```python
   from django.contrib.auth.models import User
   u = User.objects.get(username='admin')
   u.username = 'new_username_here'
   u.set_password('new_password_here')
   u.save()
   exit()
   ```

---

## 🖥️ Part 2: Page-by-Page Operational Guide

### 📊 1. Financial Overview (Home Page)
* **Description:** The corporate executive dashboard showing the overall financial health of the business.
* **Visual Components:** 4 scorecard cards (Revenue, Expenses, Profits, Margins), a monthly trends combo line/column chart overlaying revenue with margins, market split donut charts, and a table showing top showrooms by sales.
* **Business Purpose:** Gives the C-suite an immediate, high-level pulse check on national sales performance.

### 🏬 2. Showroom Leaderboard
* **Description:** An audit and compliance page for the 200 showrooms.
* **Visual Components:** KPIs tracking total showrooms, average commissions, YTD commissions volume, and a horizontal bar chart displaying showrooms with excessively high payout ratios (outliers). It includes a **live search text input** to filter showrooms client-side.
* **Business Purpose:** Helps audit dealer networks and identify franchise payout leakages.

### 👥 3. Customer Segments
* **Description:** A demographics analyzer for the buyer database.
* **Visual Components:** Cards showing registered customer base size and highest segment average order value (AOV). It features a payment methods share donut chart, a financing bank market share column chart, and a segment contribution table.
* **Business Purpose:** Helps marketing and sales teams identify who is buying their cars, how they pay, and which banks finance the transactions.

### 🌍 4. Regional Drill-Down Hub
* **Description:** A geographic operations drill-down console.
* **Visual Components:** An interactive dropdown selector to filter by region. It dynamically filters state-level sales bar charts (widened to 70% width with visible labels) and lists top regional showrooms.
* **Business Purpose:** Helps regional managers optimize inventory allocation and identify sales gaps in local states.

### 🎛️ 5. Scenario Simulator
* **Description:** An interactive planning tool that lets you run "what-if" operational scenarios.
* **Visual Components:** Sliders to cap dealer commissions, adjust logistics costs, and adjust marketing budgets. It features simulated KPI cards that recalculate instantly in the browser and a baseline-vs-simulated comparison chart.
* **Business Purpose:** Helps executives test cost-cutting strategies and immediately see the impact on bottom-line earnings.

### 🚘 6. Vehicle Inventory
* **Description:** A product catalog and fleet safety analyzer.
* **Visual Components:** Fleet-wide safety average scorecard, sales share donuts by body categories (SUV, Hatchback, Sedan, etc.), fuel option column charts, and a details specifications ledger.
* **Business Purpose:** Helps product managers and manufacturing planners track shifts in customer tastes (e.g., transition to CNG/Electric) and manage fleet safety.

---

## 📈 Part 3: Executive KPI Catalog

| Page Name | KPI Name | Description | Mathematical Formula / Source | Corporate Target |
| :--- | :--- | :--- | :--- | :--- |
| **Financial Overview** | **Gross Revenue** | Total gross billing value generated. | Sum of `total_revenue` in `monthly_finance_summary.csv` | **>$12.0B** |
| **Financial Overview** | **Operating Expenses** | Total manufacturing, logistics, marketing, and commissions. | Sum of `total_expenses` in `monthly_finance_summary.csv` | **<$8.5B** |
| **Financial Overview** | **Corporate Net Earnings**| Net operating profit. | `Gross Revenue - Operating Outflows` | **>$5.5B** |
| **Financial Overview** | **Operating Net Margin** | Margin percentage of gross revenues. | `(Net Earnings / Gross Revenue) * 100` | **>45.0%** (Current: **53.8%**) |
| **Showrooms** | **Audited Showrooms** | Active franchise networks. | Count of unique `dealer_id` in `dealer_dealers.csv` | **200 Networks** |
| **Showrooms** | **Avg Payout Ratio** | Average commissions paid. | Mean of `payout_ratio_pct` in `dealer_performance_summary.csv` | **<15.0%** (Current: **15.7%**) |
| **Showrooms** | **Critical Outliers** | Showrooms with payout ratio > 20%.| Count of showrooms where `payout_ratio_pct > 20.0%` | **0 Flagged** (Current: **54 Flagged**) |
| **Customer Segments** | **Mapped Buyer Base** | Mapped registered customers. | Count of unique `customer_id` in `customer_customers.csv` | **5,000 Customers** |
| **Customer Segments** | **Highest Segment AOV** | Average transaction value. | Max of `average_order_value` in `customer_segment_summary.csv` | **>$1.5M** |
| **Regional Hub** | **Regional Sales Revenue**| Gross revenue generated in region. | Sum of `net_amount` matching active `region` filter | **>$2.0B** |
| **Vehicle Inventory** | **Fleet Safety Rating** | Fleet-wide safety score. | Mean of `safety_rating` in `vehicle_variants.csv` | **>4.0 Stars** (Current: **4.2**) |

---

## 💡 Part 4: C-Suite Actionable Strategic Insights

### 🔴 1. Standardize a 20% Commissions Cap to Save $112M YTD
* **Observation:** The average commission ratio is **15.7%**, but **54 showrooms** exceed a critical threshold, pocketing ratios as high as **21% to 26%** of revenue.
* **C-Suite Action:** Renegotiate dealer contracts and implement a standard **20% payout cap** (audited in real-time under Page 5). This directly reclaims **$112.5M** in opex YTD, boosting net margins to **54.5%** with zero impact on sales volumes.

### 💳 2. Leverage SBI & HDFC Volume for Bulk Merchant Fee Rebates
* **Observation:** **85.2%** of all orders are financed. **SBI** and **HDFC** process **72%** of these retail loans.
* **C-Suite Action:** Negotiate a bulk routing discount with SBI and HDFC for a **0.5% transaction fee reduction**. Given our scale, this routing rebate generates **$50M+** in annual bottom-line savings.

### 👥 3. Cross-Sell Premium Addons to High AOV Budget Buyers
* **Observation:** The **Budget** segment registers the highest Average Order Value (**$1.81M**) because they purchase high-spec models (like Hybrid/CNG automatics) rather than basic trims.
* **C-Suite Action:** Target budget buyers with customized high-margin addon bundles (extended warranty packages, luxury floor liners) during booking to maximize checkout ticket sizes.

### 🌍 4. Shift Inventory Shipments from Central to North States
* **Observation:** The **North region** dominates with **36.5%** of national orders (2,559 orders). The **Central region** lags heavily at only **10.1%** (711 orders).
* **C-Suite Action:** Direct logistics channels to divert incoming vehicles from Central yards to Delhi/Punjab depots, reducing vehicle storage holdings costs and accelerating inventory turnovers.

### 🔋 5. De-escalate Diesel Assembly lines in Favor of CNG & EV Trims
* **Observation:** CNG and Electric vehicles now combine to represent **32%** of total unit volume (1,480 CNG and 780 EV units), far outstripping Diesel (156 units).
* **C-Suite Action:** Wind down diesel manufacturing allocations. Shift component sourcing budgets to increase EV SUV assembly capacity, directly matching green market demands.
