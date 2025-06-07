
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


df = pd.read_csv("ds_salaries.csv")
df.head()
connection = sqlite3.connect("salaries.db")
df.to_sql(name="salaries", con=connection)

llm = OllamaLLM(model="llama3",temperature=0)

db = SQLDatabase.from_uri("sqlite:///salaries.db")
df = pd.read_sql_query("SELECT * FROM salaries LIMIT 10", connection)

#data_queried = df.to_csv(index=False)

data_queried = df.to_json(orient="records", lines=True)
print(data_queried)
print("checking with the data analyst")
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
print("generating the report writer")
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
    description="Analyze the data from the database and write an analysis for {query}.",
    expected_output="Detailed analysis text",
    agent=data_analyst,
    context =[data_queried],
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
    verbose=False,
    memory=False,
    output_log_file="crew.log",
)

inputs = {
    "query": "Effects on salary (in USD) based on company location, size and employee experience"
}
print ("kicking off the crew")
result = crew.kickoff(inputs=inputs)

print(result)

inputs = {
    "query": "How is the `Machine Learning Engineer` salary in USD is affected by remote positions"
}

result = crew.kickoff(inputs=inputs)

print(result)

# ## References
# 
# - [DS Salaries Dataset](https://huggingface.co/datasets/Einstellung/demo-salaries)


