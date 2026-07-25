from src.database.connection import db_connector

if __name__ == "__main__":
    print("--- Starting Database Connection Test ---")
    
    # This calls the test_connection() function we wrote in src/database/connection.py
    success = db_connector.test_connection()
    
    if success:
        print("\n[RESULT] SUCCESS! Python successfully connected to your PostgreSQL database.")
    else:
        print("\n[RESULT] FAILED! Python could not connect to your PostgreSQL database.")
        print("-> Please check reports/project.log for the detailed error message.")
    
    print("-----------------------------------------")
