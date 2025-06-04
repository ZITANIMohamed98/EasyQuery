from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

PREDICT_SQL_URL = os.getenv("PREDICT_SQL_URL", "http://localhost:8001/predict_sql")
SQLTOOLS_URL = os.getenv("SQLTOOLS_URL", "http://localhost:8002/run_query")
USE_MOCKS = os.getenv("USE_MOCKS", "false").lower() == "true"

class InputQuery(BaseModel):
    user_input: constr(min_length=3, max_length=300)
    user_id: constr(min_length=1)

@app.post("/process")
def process_query(input_data: InputQuery):
    # Step 1: Try real request, if not - fallback to mock
    if USE_MOCKS:
        # MOCK: predict_sql + SQLTools
        sql_query = "SELECT * FROM trips WHERE city='Seattle'"
        result = [{"trip_id": 123, "city": "Seattle"}]
        return {"sql": sql_query, "result": result}

    # Try real predict_sql
    try:
        predict_resp = requests.post(PREDICT_SQL_URL, json=input_data.dict())
        predict_resp.raise_for_status()
        sql_query = predict_resp.json().get("sql")
    except Exception as e:
        # Fallback: mock predict_sql
        sql_query = "SELECT * FROM trips WHERE city='Seattle'"
        # Możesz logować: print(f"Falling back to mock SQL: {e}")

    if not sql_query:
        raise HTTPException(status_code=400, detail="No SQL generated")

    # Try real SQLTools
    try:
        sqltools_resp = requests.post(SQLTOOLS_URL, json={
            "query": sql_query,
            "user_id": input_data.user_id
        })
        sqltools_resp.raise_for_status()
        result = sqltools_resp.json().get("data")
    except Exception as e:
        # Fallback: mock SQLTools
        result = [{"trip_id": 123, "city": "Seattle"}]
        # Możesz logować: print(f"Falling back to mock result: {e}")

    return {
        "sql": sql_query,
        "result": result
    }
