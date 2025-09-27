from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from agents.graph import AgenticCRUDApp

app = FastAPI(
    title="Agentic CRUD API",
    description="Natural Language CRUD Operations with Human-in-the-Loop",
    version="1.0.0"
)

crud_agent = AgenticCRUDApp()

# Templates folder setup
templates = Jinja2Templates(directory="templates")

# Request schema
class QueryRequest(BaseModel):
    input: str
    human_verified: Optional[bool] = None

# Serve UI
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API endpoint
@app.post("/query")
async def query(request: QueryRequest):
    result = crud_agent.run_agent({
        "input": request.input,
        "human_verified": request.human_verified
    })
    return {
        "final_answer": result.get("answer"),
        "validated_query": result.get("validated_query")
    }
