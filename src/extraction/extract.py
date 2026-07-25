import os
from typing import List, Optional
import pandas as pd
from sqlalchemy import text

from src.database.connection import db_connector
from src.utils.helpers import time_it, save_dataframe
from src.utils.logger import setup_logger

# Initialize logger for data extraction
logger = setup_logger("extraction")

@time_it
def extract_table(table_name: str, custom_query: Optional[str] = None) -> pd.DataFrame:
    """
    Extracts data from a PostgreSQL table or runs a custom SQL query 
    and returns a Pandas DataFrame.
    
    Args:
        table_name (str): Name of the table (used for logging).
        custom_query (str, optional): Custom SQL query to execute. 
                                      If None, extracts the entire table.
                                      
    Returns:
        pd.DataFrame: DataFrame containing the extracted data.
    """
    engine = db_connector.get_engine()
    
    # Define query
    query = custom_query if custom_query else f"SELECT * FROM {table_name}"
    
    logger.info(f"Extracting data for table: '{table_name}'...")
    
    try:
        # Use pandas read_sql_query with sqlalchemy engine
        df = pd.read_sql_query(sql=text(query), con=engine)
        logger.info(f"Successfully extracted {len(df)} rows and {len(df.columns)} columns for table '{table_name}'.")
        return df
    except Exception as e:
        logger.error(f"Error extracting table '{table_name}': {e}")
        # Return an empty DataFrame on failure so the pipeline doesn't crash completely
        return pd.DataFrame()

def run_extraction_pipeline(tables_to_extract: List[str]) -> None:
    """
    Coordinates the extraction of multiple tables from the database
    and saves each one as a raw CSV file in 'data/raw/'.
    
    Args:
        tables_to_extract (List[str]): List of table names to extract.
    """
    logger.info("Starting Retailmart Finance Analytics Extraction Pipeline.")
    
    # Test connection first to verify credentials
    if not db_connector.test_connection():
        logger.critical("Database connection test failed. Aborting extraction pipeline.")
        return
        
    success_count = 0
    
    for table in tables_to_extract:
        # 1. Extract table
        df = extract_table(table_name=table)
        
        if df.empty:
            logger.warning(f"Skipping save for table '{table}' as the extracted data was empty.")
            continue
            
        # 2. Define path to data/raw/, formatting schema-qualified table name (e.g. sales_transaction.orders -> sales_transaction_orders.csv)
        safe_filename = f"{table.replace('.', '_')}.csv"
        raw_filepath = os.path.join("data", "raw", safe_filename)
        
        # 3. Save table
        save_success = save_dataframe(df=df, filepath=raw_filepath)
        if save_success:
            success_count += 1
            
    logger.info(f"Extraction Pipeline completed. Successfully extracted and saved {success_count}/{len(tables_to_extract)} tables.")

if __name__ == "__main__":
    # Actual Retailmart Finance Database tables to extract
    tables_list = [
        "customer.customers",
        "dealer.dealers",
        "dealer_network.dealer_commissions",
        "dealer_network.dealer_targets",
        "dealer_network.regional_offices",
        "finance_accounting.dealer_payouts",
        "finance_accounting.gl_accounts",
        "finance_accounting.ledger_entries",
        "finance_accounting.tax_records",
        "location_reference.cities",
        "location_reference.states",
        "pricing_management.price_master",
        "product_management.vehicle_models",
        "product_management.vehicle_variants",
        "sales_transaction.invoices",
        "sales_transaction.order_items",
        "sales_transaction.orders",
        "sales_transaction.payments"
    ]
    
    # Run the pipeline
    run_extraction_pipeline(tables_to_extract=tables_list)
