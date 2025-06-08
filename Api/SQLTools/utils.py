

#this is one time thing to set up the schemas to fill the tables with initial data
# def fill_the_tables(db_name: str):
#     # Create a database connection
#     print("Initiating database transaction...")
#     DATABASE_URL = os.getenv("DATABASE_URL"+db_name)
#     if not DATABASE_URL:
#         print("Error: DATABASE_URL environment variable is not set.")
#         return []
#     engine = create_engine(DATABASE_URL)
    
#     # fetch the list of tables in the database 
#     inspector = inspect(engine)
#     tables = inspector.get_table_names()
#     if not tables:
#         print("No tables found in the database.")
#         return []
#     # fetch the headers for each table
#     else:
#         headers = {}
#         for table in tables:
#             # adding the 
#             inspector = inspect(engine)
#             columns = inspector.get_columns(table)
#             headers[table] = [column["name"] for column in columns]
#         return headers


#     pass