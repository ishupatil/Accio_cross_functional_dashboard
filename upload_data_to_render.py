import os
import sys
import pandas as pd
from sqlalchemy import create_engine, text

MAPPING = {
    "customer_customers": "customer.customers",
    "dealer_dealers": "dealer.dealers",
    "dealer_network_dealer_commissions": "dealer_network.dealer_commissions",
    "dealer_network_dealer_targets": "dealer_network.dealer_targets",
    "dealer_network_regional_offices": "dealer_network.regional_offices",
    "finance_accounting_dealer_payouts": "finance_accounting.dealer_payouts",
    "finance_accounting_gl_accounts": "finance_accounting.gl_accounts",
    "finance_accounting_ledger_entries": "finance_accounting.ledger_entries",
    "finance_accounting_tax_records": "finance_accounting.tax_records",
    "location_reference_cities": "location_reference.cities",
    "location_reference_states": "location_reference.states",
    "pricing_management_price_master": "pricing_management.price_master",
    "product_management_vehicle_models": "product_management.vehicle_models",
    "product_management_vehicle_variants": "product_management.vehicle_variants",
    "sales_transaction_invoices": "sales_transaction.invoices",
    "sales_transaction_orders": "sales_transaction.orders",
    "sales_transaction_order_items": "sales_transaction.order_items",
    "sales_transaction_payments": "sales_transaction.payments",
}

SCHEMAS = [
    "customer",
    "dealer",
    "dealer_network",
    "finance_accounting",
    "location_reference",
    "pricing_management",
    "product_management",
    "sales_transaction"
]

def main():
    if len(sys.argv) < 2:
        print("Error: Missing External Database URL.")
        print("Usage: python upload_data_to_render.py \"your_external_database_url_here\"")
        sys.exit(1)
        
    db_url = sys.argv[1]
    
    # SQLAlchemy expects postgresql:// instead of postgres://
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    print("Connecting to live Render PostgreSQL database...")
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            # Test connection
            conn.execute(text("SELECT 1"))
            print("Connection successful!")
            
            # Create Schemas
            print("Creating PostgreSQL schemas...")
            for schema in SCHEMAS:
                conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema};"))
            # Commit schema creations
            conn.commit()
            print("All schemas verified/created.")
            
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        sys.exit(1)
        
    # Upload tables
    processed_dir = "data/processed"
    print("\nStarting dataset uploads...")
    
    for csv_name, db_table in MAPPING.items():
        csv_path = os.path.join(processed_dir, f"{csv_name}.csv")
        if not os.path.exists(csv_path):
            print(f"Warning: File {csv_path} not found. Skipping.")
            continue
            
        print(f"Loading {csv_name}.csv...")
        df = pd.read_csv(csv_path)
        
        # Parse schema and table name
        schema_name, table_name = db_table.split('.')
        
        print(f"Uploading {len(df)} rows to {db_table} on Render...")
        try:
            # Upload using pandas to_sql
            df.to_sql(
                name=table_name,
                con=engine,
                schema=schema_name,
                if_exists="replace",
                index=False
            )
            print(f"Successfully uploaded {db_table}!")
        except Exception as e:
            print(f"Error uploading {db_table}: {e}")
            
    print("\nAll database tables successfully loaded to Render PostgreSQL!")

if __name__ == "__main__":
    main()
