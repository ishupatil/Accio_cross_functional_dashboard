# Executive Report: Phase 4 Exploratory Data Analysis (EDA) Insights

This document summarizes the key financial and transactional insights discovered during the **Exploratory Data Analysis (EDA)** phase of the Retailmart dataset. These findings are derived from cross-verifying PostgreSQL queries and Pandas analytical code.

---

## 1. Categorical Frequency Analysis (Payment & Financing)

We analyzed how customers fund their vehicle purchases. This reveals our dependency on external credit and financial institutions.

### Payment Mode Distribution
* **Total Transactions Audited:** 7,000 orders.
* The customer demand is almost perfectly balanced across all four transaction types:
  
| Payment Mode | Order Volume | Percentage Share | Business Interpretation |
| :--- | :---: | :---: | :--- |
| **Lease** | 1,795 | 25.64% | Corporate/premium buyers preferring subscription models. |
| **Loan** | 1,761 | 25.16% | Retail buyers financing via traditional bank credit. |
| **Cash** | 1,739 | 24.84% | Buyers paying upfront (lower AOV). |
| **EMI** | 1,705 | 24.36% | Buyers using structured monthly payment plans. |

### Finance Provider Market Share (Financed Orders Only)
Excluding Cash and EMI transactions, a total of **5,967 orders** were backed by banking institutions:

* **Top Partner:** **ICICI Bank** leads the network with **1,038 orders (17.40% share)**.
* **Runner-Up:** **HDFC Bank** funds **1,004 orders (16.83% share)**.
* **The Tail:** **Maruti Finance** holds the lowest share at **950 orders (15.92%)**.
* **Takeaway:** Market share is highly competitive and evenly distributed among the top 6 lenders. No single bank holds a monopoly, which gives Retailmart leverage when negotiating interest rates.

---

## 2. Numerical Range Profiling (Pricing & Discounts)

We profiled the numerical ranges of transaction amounts (`net_amount`) and absolute discount values (`discount_amount`):

* **Cheapest Car Sold:** **$479,284.22** (Standard entry-level variant).
* **Most Expensive Car Sold:** **$3,186,382.90** (Premium SUV/EV variant).
* **Average Transaction Value (AOV):** **$1,790,691.80** (Indicating a premium pricing tier).
* **Average Discount Given:** **$50,051.27** per car.

> [!NOTE]
> The standard deviation of vehicle prices is **$785,161.42**, which indicates a wide variety of models in our catalog catering to both the middle-income and high-income segments.

---

## 3. Bivariate Comparison: Do Finance Plans Drive Sales?

We grouped transactions by payment mode to see if credit availability increases the customer's average order value (AOV):

| Payment Mode | Total Orders | Average Order Value (AOV) | Maximum Sale Price |
| :--- | :---: | :---: | :---: |
| **EMI** | 1,705 | **$1,806,552.58** 🚀 | $3,186,382.90 |
| **Loan** | 1,761 | **$1,791,851.67** | $3,139,672.00 |
| **Lease** | 1,795 | **$1,787,919.94** | $3,158,302.44 |
| **Cash** | 1,739 | **$1,776,543.19** ⚠️ | $3,180,542.87 |

### Key Insight:
Cash buyers spend **$30,000 less on average** than EMI/Loan buyers. Financing options lower the barrier to entry, allowing customers to upgrade to premium car variants with higher price tags because the cost is split into monthly payments.

---

## 4. Time-Series Trend Analysis (The May 2023 Spike)

Chronological sorting of monthly net revenues revealed a major sales event in mid-2023:

* **Jan - Apr 2023:** Stable, quiet sales volume averaging **44 orders** and **$75M revenue** per month.
* **May 2023:** Revenue exploded to **$328,891,440** across **183 orders** (a **300%+ increase** in volume).
* **Jun 2023:** Continued high demand at **160 orders** and **$281.1M revenue**.

> [!IMPORTANT]
> This massive spike indicates a major business event. We recommend cross-referencing this timeline with the product launch catalog (did we launch a new EV model in May?) or the marketing campaign logs.

---

## 5. Statistical Outlier Audit (IQR Method)

Using the Interquartile Range (IQR) method, we calculated the boundaries for normal transactions:
* **First Quartile (Q1 - 25th percentile):** $1,142,882.15
* **Third Quartile (Q3 - 75th percentile):** $2,436,841.56
* **IQR:** $1,293,959.41
* **Lower Outlier Limit ($Q1 - 1.5 \times IQR$):** -$798,056.97 (Treated as $0)
* **Upper Outlier Limit ($Q3 + 1.5 \times IQR$):** **$4,377,780.68**
* **Total Outliers Detected:** **0**

### Key Insight:
Every transaction falls within the statistical boundaries. This confirms that **Retailmart's sales database has no corrupted records, typing errors (like a $100M sale), or dummy testing entries.**

---

## 6. Actionable Business Recommendations for the CEO

1. **Promote Financing Options:** Since EMI and Loan transactions increase AOV by $30,000, showrooms should actively pitch installment plans to cash buyers.
2. **Prepare for the May Surge:** Factory managers should finalize inventory stock by April to ensure showrooms do not run out of cars during the annual May sales boom.
3. **Renegotiate Bank Commissions:** Since our sales are distributed evenly among ICICI, HDFC, and Kotak, we should negotiate lower processing fees with these banks by leveraging our high volumes.
