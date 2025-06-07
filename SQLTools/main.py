# using sqlalchemy to connect to a database and execute a query
import os
import sys  
from sqlalchemy import create_engine, text
# based on user Id, read the database_access.json file to check which department the user belongs to and get the databases list
def read_database_access_file(user_id):
    # Assuming the database access file is in JSON format
    import json
    
    try:
        with open('database_access.json', 'r') as file:
            data = json.load(file)
            return data.get(user_id, {}).get('databases', [])
    except FileNotFoundError:
        print("Database access file not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error decoding JSON from database access file.")
        sys.exit(1)



# Create a database connection
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Ensure the DATABASE_URL environment variable is set before running the script
if not DATABASE_URL:
    print("Error: DATABASE_URL environment variable is not set.")
#select the database 

# This script connects to a database and executes a SQL query passed as a command line argument.
def execute_query(query, params=None):
    with engine.connect() as connection:
        result = connection.execute(text(query), params)
        return result.fetchall()
    
# def main():
#     if len(sys.argv) < 2:
#         print("Usage: python main.py <SQL_QUERY>")
#         sys.exit(1)
    
#     query = sys.argv[1]
    
#     try:
#         results = execute_query(query)
#         for row in results:
#             print(row)
#     except Exception as e:
#         print(f"An error occurred: {e}")