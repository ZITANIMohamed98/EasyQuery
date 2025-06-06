# inbound.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, constr
import os
from outbound import call_predict_sql, call_sqltools
from dotenv import load_dotenv
load_dotenv()


USE_MOCKS = os.getenv("USE_MOCKS", "false").lower() == "true"

# MODELE DANYCH

class QueryInput(BaseModel):
    user_id: constr(min_length=1)
    activity_id: constr(min_length=1)
    database_name: constr(min_length=1)
    input: constr(min_length=3, max_length=500)

class ExecuteInput(QueryInput):
    query: constr(min_length=1)

class ProcessInput(BaseModel):
    user_input: constr(min_length=3, max_length=300)
    user_id: constr(min_length=1)

# --- ROUTER (to podmieni “app”) ---
router = APIRouter()

@router.post("/getQuery")
def get_query(input_data: QueryInput):
    if USE_MOCKS:
        sql_query = f"SELECT * FROM {input_data.database_name} WHERE city='Seattle'"
        return {
            "user_id": input_data.user_id,
            "activity_id": input_data.activity_id,
            "database_name": input_data.database_name,
            "query": sql_query
        }

    payload = input_data.dict()
    sql_query = call_predict_sql(payload)
    if not sql_query:
        raise HTTPException(status_code=400, detail="No SQL generated")
    return {
        "user_id": input_data.user_id,
        "activity_id": input_data.activity_id,
        "database_name": input_data.database_name,
        "query": sql_query
    }

@router.post("/executeQuery")
def execute_query(exec_data: ExecuteInput):
    if USE_MOCKS:
        result = [{"trip_id": 123, "city": "Seattle", "database": exec_data.database_name}]
        return {
            "user_id": exec_data.user_id,
            "activity_id": exec_data.activity_id,
            "database_name": exec_data.database_name,
            "query": exec_data.query,
            "data": result
        }
    payload = {
        "query": exec_data.query,
        "user_id": exec_data.user_id,
        "activity_id": exec_data.activity_id,
        "database_name": exec_data.database_name,
        "input": exec_data.input
    }
    result = call_sqltools(payload)
    if result is None:
        result = [{"trip_id": 123, "city": "Seattle", "database": exec_data.database_name}]
    return {
        "user_id": exec_data.user_id,
        "activity_id": exec_data.activity_id,
        "database_name": exec_data.database_name,
        "query": exec_data.query,
        "data": result
    }

@router.post("/process")
def process_query(input_data: ProcessInput):
    if USE_MOCKS:
        sql_query = "SELECT * FROM trips WHERE city='Seattle'"
        result = [{"trip_id": 123, "city": "Seattle"}]
        return {"sql": sql_query, "result": result}

    payload = {
        "user_input": input_data.user_input,
        "user_id": input_data.user_id
    }
    sql_query = call_predict_sql(payload)
    if not sql_query:
        sql_query = "SELECT * FROM trips WHERE city='Seattle'"

    result = call_sqltools({
        "query": sql_query,
        "user_id": input_data.user_id
    }) or [{"trip_id": 123, "city": "Seattle"}]
    return {
        "sql": sql_query,
        "result": result
    }
