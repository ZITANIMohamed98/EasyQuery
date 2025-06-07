# outbound.py
import os
import requests


PREDICT_SQL_URL = os.getenv("PREDICT_SQL_URL", "http://localhost:8001/predict_sql")
SQLTOOLS_URL = os.getenv("SQLTOOLS_URL", "http://localhost:8002/run_query")

def call_predict_sql(payload):
    """Wysyła zapytanie do usługi predict_sql"""
    try:
        resp = requests.post(PREDICT_SQL_URL, json=payload)
        resp.raise_for_status()
        return resp.json().get("sql")
    except Exception as e:
        # Możesz rozwinąć logowanie lub obsługę błędów tu
        return None

def call_sqltools(payload):
    """Wysyła zapytanie do SQLTools"""
    try:
        resp = requests.post(SQLTOOLS_URL, json=payload)
        resp.raise_for_status()
        return resp.json().get("data")
    except Exception as e:
        # Możesz rozwinąć logowanie lub obsługę błędów tu
        return None
