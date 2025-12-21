# main.py
from fastapi import FastAPI
from src.api.v1.endpoints import tasks

app = FastAPI()

app.include_router(tasks.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI + uv!"}
