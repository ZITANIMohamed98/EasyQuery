from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
import requests
import os

app = FastAPI()

# Config - docelowo lepiej przenieść to do .env
PREDICT_SQL_URL = os.getenv("PREDICT_SQL_URL", "http://localhost:8001/predict_sql")
SQLTOOLS_URL = os.getenv("SQLTOOLS_URL", "http://localhost:8002/run_query")

class InputQuery(BaseModel):
    user_input: constr(min_length=3, max_length=300)
    user_id: constr(min_length=1)

@app.post("/process")
def process_query(input_data: InputQuery):
    try:
        predict_resp = requests.post(PREDICT_SQL_URL, json=input_data.dict())
        predict_resp.raise_for_status()
        sql_query = predict_resp.json().get("sql")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SQL Prediction Error: {str(e)}")

    if not sql_query:
        raise HTTPException(status_code=400, detail="No SQL generated")

    try:
        sqltools_resp = requests.post(SQLTOOLS_URL, json={
            "query": sql_query,
            "user_id": input_data.user_id
        })
        sqltools_resp.raise_for_status()
        result = sqltools_resp.json().get("data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SQL Execution Error: {str(e)}")

    return {
        "sql": sql_query,
        "result": result
    }
