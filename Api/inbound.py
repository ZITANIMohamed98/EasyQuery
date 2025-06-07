# inbound.py
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, constr
import os
from outbound import call_predict_sql, call_sqltools
from dotenv import load_dotenv
from AI.TexttoSqlAgent.models import getQueryModel, listAllowedDbModel
from AI.AnalyzersCrew.models import executeQueryModel

from AI.TexttoSqlAgent.main import text_to_sql

load_dotenv()


USE_MOCKS = os.getenv("USE_MOCKS", "false").lower() == "true"



# --- ROUTER (to podmieni “app”) ---
router = APIRouter()

# @router.get("/getDummy")
# def get_dummy():
#     return "This is a dummy response from /getdummy"
# adding the route that reads the getQueryModel type and invokes sqltotext method to get the sql query
#    = getQueryModel("tetet","63536725-2b3c-4f8d-9f1e-0a1b2c3d4e5f",'test_db','SELECT * FROM test_table')

@router.post("/getQuery")
async def get_query(request: Request):
    data = await request.json()
    # Deserialize the request body into the getQueryModel
    # Deserialize the data into the getQueryModel
    getQuerydata = getQueryModel(
         user_id=data["user_id"],
         activity_id=data["activity_id"],
         database_name=data["database_name"],
         input=data["input"]
    )
    # deserialize the data into the getQueryModel
    # Call the text_to_sql function to generate the SQL query
    sql_query = text_to_sql(getQuerydata)
    return data["activity_id"]


@router.get("/listAllowedDbs")
def list_allowed_dbs(request: Request):
    user_id = request.query_params.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # Example: fetch allowed databases for the user (mocked here)
    allowed_dbs = ["trips", "users", "orders"]
    db_model = listAllowedDbModel(
        user_id=user_id, 
        database_list=allowed_dbs
        )
    return {
        "user_id": db_model.user_id,
        "allowed_databases": db_model.database_list
    }


@router.post("/executeQuery")
async def execute_query(request: Request):
    data = await request.json()
    # Create an instance of exesscuteQueryModel from the request data
    exec_model = executeQueryModel(
        user_id=data.get("user_id"),
        activity_id=data.get("activity_id"),
        database_name=data.get("database_name"),
        input=data.get("input")
    )

    # Example: mock result for demonstration
    result = {
        "user_id": exec_model.user_id,
        "activity_id": exec_model.activity_id,
        "database_name": exec_model.database_name,
        "input": exec_model.input,
        "output": "Query executed successfully (mocked)"
    }
    return result





#     if USE_MOCKS:
#         result = [{"trip_id": 123, "city": "Seattle", "database": exec_data.database_name}]
#         return {
#             "user_id": exec_data.user_id,
#             "activity_id": exec_data.activity_id,
#             "database_name": exec_data.database_name,
#             "query": exec_data.query,
#             "data": result
#         }
#     payload = {
#         "query": exec_data.query,
#         "user_id": exec_data.user_id,
#         "activity_id": exec_data.activity_id,
#         "database_name": exec_data.database_name,
#         "input": exec_data.input
#     }
#     result = call_sqltools(payload)
#     if result is None:
#         result = [{"trip_id": 123, "city": "Seattle", "database": exec_data.database_name}]
#     return {
#         "user_id": exec_data.user_id,
#         "activity_id": exec_data.activity_id,
#         "database_name": exec_data.database_name,
#         "query": exec_data.query,
#         "data": result
#     }

# # @router.post("/process")
# # def process_query(input_data: ProcessInput):
# #     if USE_MOCKS:
# #         sql_query = "SELECT * FROM trips WHERE city='Seattle'"
# #         result = [{"trip_id": 123, "city": "Seattle"}]
# #         return {"sql": sql_query, "result": result}

# #     payload = {
# #         "user_input": input_data.user_input,
# #         "user_id": input_data.user_id
# #     }
# #     sql_query = call_predict_sql(payload)
# #     if not sql_query:
# #         sql_query = "SELECT * FROM trips WHERE city='Seattle'"

# #     result = call_sqltools({
# #         "query": sql_query,
# #         "user_id": input_data.user_id
# #     }) or [{"trip_id": 123, "city": "Seattle"}]
# #     return {
# #         "sql": sql_query,
# #         "result": result
# #     }
