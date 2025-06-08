
import json
import os
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent
from typing import Any, Dict, List, Tuple, Union
import pandas as pd
from crewai import Agent, Crew, Process, Task
from langchain.schema import AgentFinish
from langchain.schema.output import LLMResult
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import langchain_community.tools as tools
from langchain_core.tools import tool
from .models import returnReportModel, executeQueryModel
import httpx

def define_crew(llm: OllamaLLM, data: pd.DataFrame) -> Crew:

    # Initialize the Crew of one data analyzer and one report generator
    data_analyst = Agent(
    role="Senior Data Analyst",
    goal="You receive data from the database developer and analyze it",
    backstory=dedent(
        """
        You have deep experience with analyzing datasets using Python.
        Your work is always based on the provided data and is clear,
        easy-to-understand and to the point. You have attention
        to detail and always produce very detailed work (as long as you need).
    """
    ),
    llm=llm,
    allow_delegation=False,
    )
    report_writer = Agent(
    role="Senior Report Editor",
    goal="Write an executive summary type of report based on the work of the analyst",
    backstory=dedent(
        """
        Your writing still is well known for clear and effective communication.
        You always summarize long texts into bullet points that contain the most
        important details.
        """
    ),
    llm=llm,
    allow_delegation=False,
    )
    
    analyze_data = Task(
    description="Analyze the data from the database and write an analysis for {query}, and these are the results: {data}",
    expected_output="Detailed analysis text",
    agent=data_analyst
    )

    write_report = Task(
        description=dedent(
            """
            Write an executive summary of the report from the analysis. The report
            must be less than 100 words.
        """
        ),
        expected_output="Markdown report",
        agent=report_writer,
        context=[analyze_data],
    )

    crew = Crew(
    agents=[data_analyst, report_writer],
    tasks=[analyze_data, write_report],
    process=Process.sequential,
    verbose=2,
    memory=False,
    output_log_file="crew.log",
)
# execute_crew_model: executeQueryModel
def generate_report() -> returnReportModel:
    """
    Generate a report based on the analysis performed by the crew.
    """

    # Initialize the LLM
    llm = OllamaLLM(
            model="llama3",
            temperature=0.7,
            max_tokens=1000
    )
    df = pd.read_csv("Api/AI/AnalyzersCrew/ds_salaries.csv")
    connection = sqlite3.connect("salaries.db")
    df.to_sql(name="salaries", con=connection)
    df = pd.read_sql_query("SELECT * FROM salaries LIMIT 10", connection)


    crew = define_crew(llm, df)
    inputs = {
        "data": df,
        "query": "Effects on salary (in USD) based on company location, size and employee experience"
    }

    result = crew.kickoff(inputs=inputs)

    return result

async def returnReport(report_model: returnReportModel):
    """
    Makes an HTTP POST request to the /returnReport endpoint using a returnReportModel instance.
    """
    data = {
        "user_id": report_model.user_id,
        "activity_id": report_model.activity_id,
        "database_name": report_model.database_name,
        "input": report_model.input,
        "output": report_model.output
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/returnReport",
            json=data
        )
        response.raise_for_status()
        return response.json()
print(generate_report())
