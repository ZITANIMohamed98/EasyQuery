from fastapi import FastAPI
from dotenv import load_dotenv

from inbound import router  # Importujemy router z inbound.py

load_dotenv()

app = FastAPI()

app.include_router(router)  # Rejestrujemy wszystkie endpointy z inbound.py
