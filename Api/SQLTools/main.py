# using sqlalchemy to connect to a database and execute a query
import os
import sys  
from sqlalchemy import create_engine, text
import json
# based on user Id, read the database_access.json file to check which department the user belongs to and get the databases list
def get_allowed_dbs(user_id: str) -> list[str]:
    """
    Reads the database_access.json file and returns the list of databases
    accessible to the user's department.
    """
    print(f"Listing databases for user {user_id}...")
    try:
        with open('database_access.json', 'r') as file:
                data = json.load(file)
        dblist = data["departments"][data["Users"][user_id]["department"]]["databases"]
        if not dblist:
            print(f"No databases found for user {user_id}.")
            return []
        else:
            return dblist
        
    except FileNotFoundError:
        print("Error: database_access.json file not found.")
        return []

def initiate_database_transaction():
    # Create a database connection
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("Error: DATABASE_URL environment variable is not set.")
        sys.exit(1)
    engine = create_engine(DATABASE_URL)
    
    # querry the tables to list the tables in the database
    with engine.connect() as connection:
        result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
        tables = [row['table_name'] for row in result]
        if not tables:
            print("No tables found in the database.")
            return []
        else:
            return tables

# This script connects to a database and executes a SQL query passed as a command line argument.
def execute_query(query, params=None):
    with engine.connect() as connection:
        result = connection.execute(text(query), params)
        return result.fetchall()
    
