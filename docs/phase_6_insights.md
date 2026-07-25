# Executive Report: Phase 6 Business Insights & Aggregations

This report compiles strategic, high-level business intelligence insights extracted by combining vehicle sales tables with customer demographics and geographic references.

---

## 1. Geographical Leaderboard (Regions & States)

We aggregated net revenues across regions to understand Retailmart's primary sales territories:

* **Top Region: North**
  * Total Orders: **2,156**
  * Total Revenue: **$3,865,042,912.44 (30.8% share)**
* **Second Region: West**
  * Total Orders: **2,042**
  * Total Revenue: **$3,654,120,490.87 (29.1% share)**
* **Third Region: South**
  * Total Orders: **1,720**
  * Total Revenue: **$3,082,104,221.11 (24.6% share)**
* **Bottom Region: East**
  * Total Orders: **1,082**
  * Total Revenue: **$1,933,581,223.58 (15.5% share)**

> [!NOTE]
> The **North** and **West** regions are the core drivers of Retailmart's business, combining to represent **60% of all revenues**. The East region represents a major expansion opportunity as it underperforms compared to other zones.

---

## 2. Showroom Leaderboard (Top 10 Showrooms)

Out of 200 showrooms in the network, these are the **Top 5 Star Dealerships** by revenue:

1. **Dada Motors Dhanbad (Jharkhand)**
   * Total Orders: 47 | Total Revenue: **$94,050,873.16**
2. **Kar Motors Chandrapur (Maharashtra)**
   * Total Orders: 50 | Total Revenue: **$92,021,301.79**
3. **Ahuja Motors Suryapet (Telangana)**
   * Total Orders: 45 | Total Revenue: **$89,153,735.34**
4. **Chaudhry Motors Bikaner (Rajasthan)**
   * Total Orders: 49 | Total Revenue: **$86,400,299.95**
5. **Nagi Motors Durgapur (West Bengal)**
   * Total Orders: 48 | Total Revenue: **$85,810,655.72**

---

## 3. Seasonal Quarterly Growth Trends (QoQ)

Calculating Quarter-over-Quarter (QoQ) revenue growth using the `LAG()` function reveals the financial growth curve:

* **2023-Q1:** **$215.39 Million** (Baseline)
* **2023-Q2:** **$701.40 Million** ($\mathbf{+225.64\%}$ QoQ growth)
  * *Analysis:* Driven by the massive sales spike in May 2023.
* **2023-Q3:** **$1.01 Billion** ($\mathbf{+44.75\%}$ QoQ growth)
* **2023-Q4:** **$1.45 Billion** ($\mathbf{+43.12\%}$ QoQ growth)
* **2024-Q1:** **$1.82 Billion** ($\mathbf{+25.32\%}$ QoQ growth)

> [!TIP]
> While sales volume continues to grow absolute-dollar-wise, the **growth percentage rate is decelerating** (slowing from +225% in Q2 down to +25% by early 2024). This indicates that the market is reaching saturation, and we must launch new variant models to kickstart growth.

---

## 4. Customer Segment Profitability

We analyzed how much revenue is driven by different customer pricing profiles:

* **Premium Segment (High-Volume Buyers):**
  * Total Orders: **3,692**
  * Total Revenue: **$6.58 Billion (52.5% share)**
  * Average Order Value (AOV): **$1,783,267.00**
* **Mid Segment:**
  * Total Orders: **2,423**
  * Total Revenue: **$4.34 Billion (34.7% share)**
  * Average Order Value (AOV): **$1,794,543.00**
* **Budget Segment:**
  * Total Orders: **885**
  * Total Revenue: **$1.60 Billion (12.8% share)**
  * Average Order Value (AOV): **$1,810,563.00**

### Key Insight:
Although the **Budget segment** has a slightly higher average order size ($1.81M vs. $1.78M) because they only buy premium variants when they finally make a purchase, the **Premium segment** is our absolute engine, driving **over half of all company revenues** due to the sheer volume of orders.

---

## 5. Executive Team Action Plan

1. **Focus Marketing on North/West:** Direct 60% of marketing and advertising campaigns to the North and West zones to protect our core revenue regions.
2. **Launch East Region Expansion:** Since the East region is performing at less than half the volume of the North, run a dealer expansion drive to sign up new showrooms in cities like Kolkata, Patna, and Guwahati.
3. **Double Down on Premium Customer Campaigns:** The Premium segment represents 52.5% of our revenue. Focus product design and EV development specifically on premium luxury variants to maintain this loyal customer group.
