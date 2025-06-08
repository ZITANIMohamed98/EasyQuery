# inbound.py
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, constr
import os
from dotenv import load_dotenv
from AI.TexttoSqlAgent.models import getQueryModel, listAllowedDbModel
from AI.AnalyzersCrew.models import executeQueryModel, returnReportModel
import asyncio
from AI.TexttoSqlAgent.main import text_to_sql
from SQLTools.main import get_allowed_dbs
from AI.AnalyzersCrew.main import returnReport

load_dotenv()


USE_MOCKS = os.getenv("USE_MOCKS", "false").lower() == "true"



# --- ROUTER (to podmieni “app”) ---
router = APIRouter()

@router.post("/getQuery")
async def get_query(request: Request):
    data = await request.json()
    print (f"Received data: {data}")
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
    sql_query = await text_to_sql(getQuerydata)
    # await asyncio.sleep(10)  # Simulate some processing delay
    return sql_query.querypredicted


@router.get("/listAllowedDbs")
async def list_allowed_dbs(user_id: str):
    print (f"Listing allowed databases for user_id: {user_id}")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    dbs = get_allowed_dbs(user_id)
    return dbs


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


    report_generated = await returnReport(exec_model)
    await asyncio.sleep(10) 
    return report_generated

