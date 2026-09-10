# Master KPI Data Dictionary & Data Lineage Guide

This document provides a detailed mapping for every Key Performance Indicator (KPI) on the dashboard. It explains the exact database schemas, tables, and columns used, along with the architectural justification for selecting each specific table.

---

## 📈 1. Corporate Financial Overview KPIs

### A. Corporate Gross Revenue ($14.84B)
* **Tables Used:**
  1. `sales_transaction.orders`
  2. `finance_accounting.ledger_entries`
  3. `finance_accounting.gl_accounts`
* **Columns Used:**
  * `orders.net_amount` (Vehicle sales invoicing)
  * `ledger_entries.credit_amount` (where `gl_accounts.account_code` = `'4100'` for Spares Income)
  * `ledger_entries.credit_amount` (where `gl_accounts.account_code` = `'4200'` for Service Income)
* **Why These Tables Were Selected:**
  * **`orders`** tracks vehicle sales ($12.53B). However, an automotive company also earns auxiliary income from spare parts sales and repair services.
  * **`ledger_entries`** and **`gl_accounts`** record double-entry accounting credits for non-vehicle revenues (Spares = $1.80B, Service = $0.50B). Combining these 3 tables provides the true top-line revenue ($14.84B).

---

### B. Total Operating Expenses / OpEx ($7.96B)
* **Tables Used:**
  1. `finance_accounting.ledger_entries`
  2. `finance_accounting.gl_accounts`
* **Columns Used:**
  * `ledger_entries.debit_amount`
  * `gl_accounts.account_code` (Codes `5000` through `5600`), `gl_accounts.account_type` (`'Expense'`)
* **Why These Tables Were Selected:**
  * **`ledger_entries`** is the general ledger containing all corporate financial debit entries.
  * Joining with **`gl_accounts`** on `account_id` allows us to filter strictly by `account_type = 'Expense'` and aggregate the 7 corporate operational cost categories: COGS (`5000`), Manufacturing (`5100`), Payroll (`5200`), Marketing (`5300`), Logistics (`5400`), Commissions (`5500`), and Administration (`5600`).

---

### C. Corporate Net Profit ($6.88B) & Operating Net Margin (46.4%)
* **Tables Used:**
  * Derived from Gross Revenue ($14.84B) and Operating Expenses ($7.96B).
* **Columns Used:**
  * Formula: `Net Profit = Gross Revenue - Operating Expenses`
  * Formula: `Net Margin % = (Net Profit / Gross Revenue) * 100`
* **Why Selected:**
  * Standard income statement profit-and-loss math evaluated dynamically in backend views.

---

## 🏬 2. Showroom & Network Operations KPIs

### A. Showroom Order Volume & Revenue ($12.53B)
* **Tables Used:**
  1. `sales_transaction.orders`
  2. `dealer.dealers`
* **Columns Used:**
  * `orders.order_id` (Count of transactions)
  * `orders.net_amount` (Sum of sales revenue)
  * `dealers.dealer_id`, `dealers.dealer_name`
* **Why These Tables Were Selected:**
  * **`orders`** records the `dealer_id` for every vehicle sold. Joining with **`dealers`** maps total sales volume and invoicing revenue directly to each individual showroom.

---

### B. Dealer Commissions ($3.86B) & Payout Ratio (%)
* **Tables Used:**
  1. `dealer_network.dealer_commissions`
  2. `sales_transaction.orders`
* **Columns Used:**
  * `dealer_commissions.total_commission`
  * `orders.net_amount`
* **Why These Tables Were Selected:**
  * **`dealer_network.dealer_commissions`** contains the official calculated commission records for each dealer.
  * We do not use `dealer_payouts` for overall performance auditing because payouts record cash disbursement dates rather than total earned commissions.

---

## 🌍 3. Regional Sales & Territory KPIs

### A. Regional Sales Breakdown (North, East, West, South, Central)
* **Tables Used (4-Table Snowflake Chain):**
  1. `sales_transaction.orders`
  2. `dealer.dealers`
  3. `location_reference.cities`
  4. `location_reference.states`
* **Columns Used:**
  * `orders.net_amount`
  * `dealers.city_id`
  * `cities.state_id`
  * `states.region`, `states.state_name`
* **Why These Tables Were Selected:**
  * **`orders`** has `dealer_id`. **`dealers`** has `city_id`. **`cities`** has `state_id`. **`states`** contains the geographic `region`.
  * This 4-table join chain links individual car sales to their parent geographic territories.

---

## 👥 4. Customer Segments & Financing KPIs

### A. Customer Buyer Base (5,000) & Segment Revenue
* **Tables Used:**
  1. `sales_transaction.orders`
  2. `customer.customers`
* **Columns Used:**
  * `customers.customer_id`, `customers.customer_segment` (`Premium`, `Mid`, `Budget`)
  * `orders.net_amount`, `orders.order_id`
* **Why These Tables Were Selected:**
  * **`customers`** stores customer demographic profiling. Joining with **`orders`** maps sales revenue and transaction counts to customer wealth tiers.

---

### B. Payment Modes (`Lease`, `Loan`, `Cash`, `EMI`) & Bank Shares
* **Tables Used:**
  1. `sales_transaction.orders`
* **Columns Used:**
  * `orders.payment_mode`
  * `orders.finance_provider` (`HDFC Bank`, `SBI`, `ICICI Bank`, etc.)
* **Why This Table Was Selected:**
  * **`orders`** records the payment method and financing provider directly at the time of sale.
  * We do not use `payments` because `payments` records individual installment receipts rather than car purchase channels.

---

## 🚘 5. Vehicle Inventory & Product Catalog KPIs

### A. Fleet Configurations (25 Models, 96 Variants, 4.2-Star Safety)
* **Tables Used:**
  1. `product_management.vehicle_models`
  2. `product_management.vehicle_variants`
* **Columns Used:**
  * `vehicle_models.model_name`, `vehicle_models.body_type`
  * `vehicle_variants.variant_name`, `vehicle_variants.safety_rating`, `vehicle_variants.fuel_type`, `vehicle_variants.engine_capacity_cc`
* **Why These Tables Were Selected:**
  * **`vehicle_models`** and **`vehicle_variants`** form the master product catalog, storing specifications and crash safety scores.
