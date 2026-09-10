import os
import pandas as pd
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from src.database.connection import db_connector

# ==========================================
# LIVE POSTGRESQL DATA AGGREGATION ENGINES
# ==========================================

def get_db_table(table_spec):
    """
    Loads a specific table directly from the PostgreSQL database into a Pandas DataFrame.
    """
    engine = db_connector.get_engine()
    return pd.read_sql_query(f"SELECT * FROM {table_spec}", con=engine)

def get_monthly_finance_summary():
    """
    Recreates the monthly finance summary dynamically by joining and aggregating
    live orders and general ledger entries from PostgreSQL.
    """
    orders_df = get_db_table("sales_transaction.orders")
    ledger_df = get_db_table("finance_accounting.ledger_entries")
    gl_accounts_df = get_db_table("finance_accounting.gl_accounts")
    
    # Process monthly vehicle sales revenues from orders
    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
    orders_df["month"] = orders_df["order_date"].dt.to_period("M").astype(str)
    monthly_rev = orders_df.groupby("month")["net_amount"].sum().reset_index()
    monthly_rev.rename(columns={"net_amount": "vehicle_revenue"}, inplace=True)
    
    # Process monthly spares, service income and opex from ledger entries
    ledger_df["transaction_date"] = pd.to_datetime(ledger_df["transaction_date"])
    merged_ledger = pd.merge(ledger_df, gl_accounts_df, on="account_id")
    merged_ledger["month"] = merged_ledger["transaction_date"].dt.to_period("M").astype(str)
    merged_ledger["cat_code"] = merged_ledger["account_code"].astype(str).str[:4]
    
    # Other Income (Spares 4100, Service 4200)
    spares = merged_ledger[merged_ledger["cat_code"] == "4100"].groupby("month")["credit_amount"].sum().reset_index(name="spares_revenue")
    service = merged_ledger[merged_ledger["cat_code"] == "4200"].groupby("month")["credit_amount"].sum().reset_index(name="service_revenue")
    
    # Expenses by Category
    expenses_df = merged_ledger[merged_ledger["account_type"] == "Expense"]
    monthly_exp_cat = expenses_df.groupby(["month", "cat_code"])["debit_amount"].sum().unstack(fill_value=0).reset_index()
    
    # Correct mapping based on gl_accounts definition
    mapping = {
        "5000": "cogs",
        "5100": "manufacturing_costs",
        "5200": "salaries_wages",
        "5300": "marketing_costs",
        "5400": "logistics_costs",
        "5500": "dealer_commissions",
        "5600": "admin_costs"
    }
    for code, col in mapping.items():
        if code not in monthly_exp_cat.columns:
            monthly_exp_cat[code] = 0.0
        monthly_exp_cat.rename(columns={code: col}, inplace=True)
        
    # Merge all revenue and expense aggregates
    summary = pd.merge(monthly_rev, spares, on="month", how="outer").fillna(0.0)
    summary = pd.merge(summary, service, on="month", how="outer").fillna(0.0)
    summary = pd.merge(summary, monthly_exp_cat, on="month", how="outer").fillna(0.0)
    summary.sort_values(by="month", inplace=True)
    
    # Compute Total Revenue (Vehicle + Spares + Service)
    summary["total_revenue"] = summary["vehicle_revenue"] + summary["spares_revenue"] + summary["service_revenue"]
    
    # Compute Total Expenses & Net Profit
    expense_cols = list(mapping.values())
    summary["total_expenses"] = summary[expense_cols].sum(axis=1)
    summary["net_profit"] = summary["total_revenue"] - summary["total_expenses"]
    summary["net_profit_margin"] = (summary["net_profit"] / summary["total_revenue"] * 100.0).fillna(0.0)
    
    return summary

def get_regional_sales_summary():
    """
    Groups regional sales contribution using live tables.
    """
    orders_df = get_db_table("sales_transaction.orders")
    dealers_df = get_db_table("dealer.dealers")
    cities_df = get_db_table("location_reference.cities")
    states_df = get_db_table("location_reference.states")
    
    merged = pd.merge(orders_df, dealers_df[['dealer_id', 'city_id']], on="dealer_id", how="left")
    merged = pd.merge(merged, cities_df[['city_id', 'state_id']], on="city_id", how="left")
    merged = pd.merge(merged, states_df[['state_id', 'region']], on="state_id", how="left")
    
    regional = merged.groupby("region")["net_amount"].sum().reset_index()
    regional.rename(columns={"net_amount": "total_revenue"}, inplace=True)
    return regional

def get_dealer_performance_summary():
    """
    Computes showroom ledger performance, mapping cities, states, and commissions dynamically.
    """
    orders_df = get_db_table("sales_transaction.orders")
    dealers_df = get_db_table("dealer.dealers")
    cities_df = get_db_table("location_reference.cities")
    states_df = get_db_table("location_reference.states")
    comm_df = get_db_table("dealer_network.dealer_commissions")
    
    orders_agg = orders_df.groupby("dealer_id").agg(
        total_orders=("order_id", "count"),
        total_revenue=("net_amount", "sum")
    ).reset_index()
    
    comm_agg = comm_df.groupby("dealer_id")["total_commission"].sum().reset_index()
    
    perf = pd.merge(dealers_df[['dealer_id', 'dealer_name', 'city_id', 'status']], orders_agg, on="dealer_id", how="left").fillna(0.0)
    perf = pd.merge(perf, comm_agg, on="dealer_id", how="left").fillna(0.0)
    
    perf["avg_order_value"] = (perf["total_revenue"] / perf["total_orders"]).fillna(0.0)
    perf["payout_ratio_pct"] = (perf["total_commission"] / perf["total_revenue"] * 100.0).fillna(0.0)
    
    perf = pd.merge(perf, cities_df[['city_id', 'state_id']], on="city_id", how="left")
    perf = pd.merge(perf, states_df[['state_id', 'state_name', 'region']], on="state_id", how="left")
    
    return perf

def get_customer_segment_summary():
    """
    Aggregates orders to segments dynamically.
    """
    orders_df = get_db_table("sales_transaction.orders")
    customers_df = get_db_table("customer.customers")
    
    merged = pd.merge(orders_df, customers_df[['customer_id', 'customer_segment']], on="customer_id", how="left")
    
    segments = merged.groupby("customer_segment").agg(
        total_orders=("order_id", "count"),
        total_revenue=("net_amount", "sum"),
        average_order_value=("net_amount", "mean")
    ).reset_index()
    return segments


# ==========================================
# VIEW CONTROLLER HANDLERS
# ==========================================

@login_required
def home(request):
    """
    Serves the Corporate Financial Overview homepage.
    Queries live PostgreSQL database and passes data lists to ApexCharts.
    """
    context = {
        "page_title": "Financial Overview",
        "page_subtitle": "National performance report & operating margins audit console",
        "total_revenue_b": 0,
        "total_expenses_b": 0,
        "total_profit_b": 0,
        "net_margin": 0,
        "months": [],
        "revenues": [],
        "margins": [],
        "regions": [],
        "region_revenues": [],
        "expense_labels": [],
        "expense_values": [],
        "top_dealers": []
    }
    try:
        # 1. Monthly Financial aggregates
        monthly_df = get_monthly_finance_summary()
        
        total_rev = float(monthly_df["total_revenue"].sum())
        total_exp = float(monthly_df["total_expenses"].sum())
        total_prof = float(monthly_df["net_profit"].sum())
        
        # Slices after 2023-04 for clean financial year reporting
        reporting_df = monthly_df[monthly_df["month"] >= "2023-04"].copy()
        reporting_df["month_date"] = pd.to_datetime(reporting_df["month"])
        reporting_df = reporting_df.sort_values(by="month_date")
        
        context["total_revenue_b"] = round(total_rev / 1e9, 2)
        context["total_expenses_b"] = round(total_exp / 1e9, 2)
        context["total_profit_b"] = round(total_prof / 1e9, 2)
        context["net_margin"] = round(reporting_df["net_profit_margin"].mean(), 1)
        
        # Chart trends (Revenues in Millions, margins in %)
        context["months"] = reporting_df["month_date"].dt.strftime("%b %y").tolist()
        context["revenues"] = (reporting_df["total_revenue"] / 1e6).round(2).tolist()
        context["margins"] = reporting_df["net_profit_margin"].round(1).tolist()
        
        # Operating Expenses breakdown calculation
        expense_cats = {
            "Commissions": float(monthly_df["dealer_commissions"].sum()),
            "Manufacturing": float(monthly_df["manufacturing_costs"].sum()),
            "COGS": float(monthly_df["cogs"].sum()),
            "Salaries & Wages": float(monthly_df["salaries_wages"].sum()),
            "Logistics": float(monthly_df["logistics_costs"].sum()),
            "Marketing": float(monthly_df["marketing_costs"].sum()),
            "Administration": float(monthly_df["admin_costs"].sum())
        }
        sorted_expenses = sorted(expense_cats.items(), key=lambda x: x[1], reverse=True)
        context["expense_labels"] = [item[0] for item in sorted_expenses]
        context["expense_values"] = [round(item[1] / 1e6, 2) for item in sorted_expenses]
        
        # 2. Regional splits
        region_df = get_regional_sales_summary()
        context["regions"] = region_df["region"].tolist()
        context["region_revenues"] = (region_df["total_revenue"] / 1e6).round(2).tolist()
        
        # 3. Mapped top 10 showrooms list
        dealer_df = get_dealer_performance_summary()
        top_10 = dealer_df.sort_values(by="total_revenue", ascending=False).head(10)
        
        top_list = []
        for _, row in top_10.iterrows():
            state = row.get("state_name", "N/A")
            if pd.isna(state):
                state = "N/A"
            top_list.append({
                "dealer_name": row["dealer_name"],
                "state_name": state,
                "total_orders": int(row["total_orders"]),
                "total_revenue": f"${row['total_revenue']/1e6:.1f}M",
                "payout_ratio_pct": round(float(row["payout_ratio_pct"]), 1)
            })
        context["top_dealers"] = top_list
            
    except Exception as e:
        print("Exception loading home view data:", e)
        
    return render(request, "dashboard/home.html", context)

@login_required
def showrooms(request):
    """
    Slices dealer performance summary from live PostgreSQL database. 
    Prepares outlier payout lists for ApexCharts bar chart and detailed showroom lists for client-side search.
    """
    context = {
        "page_title": "Showroom Leaderboard",
        "page_subtitle": "National showroom payouts audit & commissions outlier detection console",
        "total_dealers": 0,
        "avg_payout": 0,
        "total_payout_m": 0,
        "critical_count": 0,
        "showrooms_list": [],
        "outlier_names": [],
        "outlier_ratios": []
    }
    try:
        dealer_df = get_dealer_performance_summary()
        
        context["total_dealers"] = dealer_df.shape[0]
        context["avg_payout"] = round(dealer_df["payout_ratio_pct"].mean(), 1)
        context["total_payout_m"] = round(dealer_df["total_commission"].sum() / 1e6, 1)
        context["critical_count"] = dealer_df[dealer_df["payout_ratio_pct"] > 20.0].shape[0]
        
        # Sorted table data
        sorted_dealers = dealer_df.sort_values(by="total_revenue", ascending=False)
        showrooms_list = []
        for _, row in sorted_dealers.iterrows():
            showrooms_list.append({
                "dealer_name": row["dealer_name"],
                "total_orders": int(row["total_orders"]),
                "total_revenue": f"${row['total_revenue']:,.2f}",
                "total_commission": f"${row['total_commission']:,.2f}",
                "payout_ratio_pct": round(float(row["payout_ratio_pct"]), 1)
            })
        context["showrooms_list"] = showrooms_list
        
        # High commission outlier details (Top 15 ratios)
        outliers = dealer_df.sort_values(by="payout_ratio_pct", ascending=False).head(15)
        context["outlier_names"] = outliers["dealer_name"].tolist()
        context["outlier_ratios"] = outliers["payout_ratio_pct"].round(1).tolist()
    except Exception as e:
        print("Exception in showrooms view:", e)
        
    return render(request, "dashboard/showrooms.html", context)

@login_required
def customers(request):
    """
    Slices segments and orders datasets from live PostgreSQL database to calculate payment modes, bank shares, and segment AOV matrix.
    """
    context = {
        "page_title": "Customer Segments",
        "page_subtitle": "Customer spending profiles, transaction channels, & bank financing shares",
        "total_buyers": 0,
        "dominant_segment": "Premium",
        "highest_aov": "$1.81M",
        "payment_modes": [],
        "payment_counts": [],
        "banks": [],
        "bank_counts": [],
        "segments_list": []
    }
    try:
        customers_df = get_db_table("customer.customers")
        context["total_buyers"] = customers_df.shape[0]
            
        orders_df = get_db_table("sales_transaction.orders")
        
        # Payment mode donut data
        pay_counts = orders_df["payment_mode"].value_counts()
        context["payment_modes"] = pay_counts.index.tolist()
        context["payment_counts"] = pay_counts.values.tolist()
        
        # Financing bank column data
        finance_df = orders_df[orders_df["finance_provider"] != "Self-Financed"]
        bank_counts = finance_df["finance_provider"].value_counts()
        context["banks"] = bank_counts.index.tolist()
        context["bank_counts"] = bank_counts.values.tolist()
            
        segment_df = get_customer_segment_summary()
        segment_df = segment_df.sort_values(by="total_revenue", ascending=False)
        
        # Pull details for summary cards dynamically
        context["dominant_segment"] = segment_df.iloc[0]["customer_segment"] if not segment_df.empty else "Premium"
        
        aov_df = segment_df.sort_values(by="average_order_value", ascending=False)
        context["highest_aov"] = f"${aov_df.iloc[0]['average_order_value']/1e6:.2f}M" if not aov_df.empty else "$1.81M"
        
        segments_list = []
        for _, row in segment_df.iterrows():
            segments_list.append({
                "customer_segment": row["customer_segment"],
                "orders_count": int(row["total_orders"]),
                "revenue_sum": f"${row['total_revenue']/1e9:.2f}B",
                "aov_mean": f"${row['average_order_value']/1e6:.2f}M"
            })
        context["segments_list"] = segments_list
            
    except Exception as e:
        print("Exception in customers view:", e)
        
    return render(request, "dashboard/customers.html", context)

@login_required
def regions(request):
    """
    Geographic Segment Hub. 
    Filters states & showrooms datasets by URL region parameter (GET) using live PostgreSQL tables.
    """
    selected_region = request.GET.get("region", "North")
    context = {
        "page_title": "Regional Drill-Down",
        "page_subtitle": f"Drill-down operations & sales breakdown inside the {selected_region} region",
        "selected_region": selected_region,
        "orders_count": 0,
        "revenue_sum_m": 0.0,
        "aov_mean_m": 0.0,
        "active_dealers": 0,
        "state_names": [],
        "state_sales_m": [],
        "state_orders": [],
        "regional_top_dealers": []
    }
    try:
        orders_df = get_db_table("sales_transaction.orders")
        dealer_df = get_dealer_performance_summary()
        dealers_ref = get_db_table("dealer.dealers")
        cities_df = get_db_table("location_reference.cities")
        states_df = get_db_table("location_reference.states")
        
        # Join tables dynamically
        merged = pd.merge(orders_df, dealer_df[['dealer_id', 'dealer_name']], on="dealer_id")
        merged = pd.merge(merged, dealers_ref[['dealer_id', 'city_id']], on="dealer_id")
        merged = pd.merge(merged, cities_df[['city_id', 'state_id']], on="city_id")
        merged = pd.merge(merged, states_df[['state_id', 'state_name', 'region']], on="state_id")
        
        # Filter by selected region
        region_data = merged[merged["region"] == selected_region].copy()
        
        context["orders_count"] = region_data.shape[0]
        
        if region_data.shape[0] > 0:
            context["revenue_sum_m"] = round(float(region_data["net_amount"].sum() / 1e6), 2)
            context["aov_mean_m"] = round(float(region_data["net_amount"].mean() / 1e6), 2)
            context["active_dealers"] = region_data["dealer_id"].nunique()
            
            # State-level sales breakdown
            state_agg = region_data.groupby("state_name").agg(
                state_revenue=("net_amount", "sum"),
                state_orders=("order_id", "count")
            ).reset_index()
            
            context["state_names"] = state_agg["state_name"].tolist()
            context["state_sales_m"] = (state_agg["state_revenue"] / 1e6).round(2).tolist()
            context["state_orders"] = state_agg["state_orders"].tolist()
            
            # Local dealer leaderboard inside this region
            local_dealers = region_data.groupby("dealer_name").agg(
                orders_count=("order_id", "count"),
                revenue_sum=("net_amount", "sum")
            ).reset_index()
            
            local_dealers = pd.merge(local_dealers, dealer_df[['dealer_name', 'payout_ratio_pct']], on="dealer_name", how="left").fillna(0.0)
            local_dealers = local_dealers.sort_values(by="revenue_sum", ascending=False).head(10)
            
            regional_top_dealers = []
            for _, row in local_dealers.iterrows():
                regional_top_dealers.append({
                    "dealer_name": row["dealer_name"],
                    "orders_count": int(row["orders_count"]),
                    "revenue_sum": f"${row['revenue_sum']/1e6:.2f}M",
                    "payout_ratio_pct": round(float(row["payout_ratio_pct"]), 1)
                })
            context["regional_top_dealers"] = regional_top_dealers
            
    except Exception as e:
        print("Exception in regions view:", e)
    return render(request, "dashboard/regions.html", context)

@login_required
def simulator(request):
    """
    Corporate operating profit simulation view.
    Calculates baselines and pre-computes commission savings lookup mapping from live PostgreSQL database.
    """
    context = {
        "page_title": "Scenario Simulator",
        "page_subtitle": "CEO what-if scenarios planner for capping commissions & logistics swings",
        "baseline_revenue_b": 0.0,
        "baseline_expenses_b": 0.0,
        "baseline_net_profit_b": 0.0,
        "baseline_margin": 0.0,
        "raw_revenue": 0.0,
        "raw_expenses": 0.0,
        "raw_net_profit": 0.0,
        "raw_logistics": 0.0,
        "raw_marketing": 0.0,
        "comm_savings_json": {}
    }
    try:
        monthly_df = get_monthly_finance_summary()
        dealer_df = get_dealer_performance_summary()
        
        # Raw variables for JS math
        rev_sum = float(monthly_df["total_revenue"].sum())
        exp_sum = float(monthly_df["total_expenses"].sum())
        prof_sum = float(monthly_df["net_profit"].sum())
        log_sum = float(monthly_df["logistics_costs"].sum())
        mkt_sum = float(monthly_df["marketing_costs"].sum())
        
        context["raw_revenue"] = rev_sum
        context["raw_expenses"] = exp_sum
        context["raw_net_profit"] = prof_sum
        context["raw_logistics"] = log_sum
        context["raw_marketing"] = mkt_sum
        
        context["baseline_revenue_b"] = round(rev_sum / 1e9, 2)
        context["baseline_expenses_b"] = round(exp_sum / 1e9, 2)
        context["baseline_net_profit_b"] = round(prof_sum / 1e9, 2)
        context["baseline_margin"] = round((prof_sum / rev_sum) * 100.0, 1)
        
        # Pre-compute commission savings lookup for caps between 5% and 30%
        comm_savings_dict = {}
        baseline_total_commissions = float(dealer_df["total_commission"].sum())
        for cap in range(5, 31):
            sim_ratio = dealer_df["payout_ratio_pct"].map(lambda x: min(x, cap))
            sim_comm = dealer_df["total_revenue"] * (sim_ratio / 100.0)
            savings = baseline_total_commissions - float(sim_comm.sum())
            comm_savings_dict[str(cap)] = round(savings, 2)
        context["comm_savings_json"] = comm_savings_dict
    except Exception as e:
        print("Exception in simulator view:", e)
    return render(request, "dashboard/simulator.html", context)

@login_required
def inventory(request):
    """
    Vehicle Inventory console.
    Calculates body type donut ratios, fuel variant splits, and builds variant catalog list from live PostgreSQL database.
    """
    context = {
        "page_title": "Vehicle Inventory",
        "page_subtitle": "Corporate vehicle variants catalog, body types, & fuel distributions",
        "total_models": 0,
        "total_variants": 0,
        "avg_safety_rating": 0.0,
        "dominant_fuel": "Petrol",
        "body_types": [],
        "body_counts": [],
        "fuel_types": [],
        "fuel_counts": [],
        "inventory_list": []
    }
    try:
        items_df = get_db_table("sales_transaction.order_items")
        variants_df = get_db_table("product_management.vehicle_variants")
        models_df = get_db_table("product_management.vehicle_models")
        
        # Merged dataset for sales aggregates
        merged = pd.merge(items_df, variants_df, on="variant_id")
        merged = pd.merge(merged, models_df, on="model_id")
        
        context["total_models"] = models_df.shape[0]
        context["total_variants"] = variants_df.shape[0]
        context["avg_safety_rating"] = round(float(variants_df["safety_rating"].mean()), 1)
        
        # Body types split
        body_counts = merged["body_type"].value_counts()
        context["body_types"] = body_counts.index.tolist()
        context["body_counts"] = body_counts.values.tolist()
        
        # Fuel types split
        fuel_counts = merged["fuel_type"].value_counts()
        context["fuel_types"] = fuel_counts.index.tolist()
        context["fuel_counts"] = fuel_counts.values.tolist()
        context["dominant_fuel"] = f"{fuel_counts.index[0]} ({fuel_counts.values[0] / fuel_counts.sum() * 100:.1f}%)"
        
        # Mapped catalog for inventory table (Sort by model name, variant name)
        catalog = pd.merge(variants_df, models_df[['model_id', 'model_name', 'body_type']], on="model_id")
        catalog = catalog.sort_values(by=["model_name", "variant_name"])
        
        inventory_list = []
        for _, row in catalog.head(35).iterrows():
            inventory_list.append({
                "model_name": row["model_name"],
                "variant_name": row["variant_name"],
                "body_type": row["body_type"],
                "fuel_type": row["fuel_type"],
                "transmission": row["transmission"],
                "engine_cc": int(row["engine_cc"]) if not pd.isna(row["engine_cc"]) else "N/A",
                "safety_rating": row["safety_rating"]
            })
        context["inventory_list"] = inventory_list
        
    except Exception as e:
        print("Exception in inventory view:", e)
        
    return render(request, "dashboard/inventory.html", context)
