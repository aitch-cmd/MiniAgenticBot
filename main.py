from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from agents.graph import AgenticCRUDApp

app = FastAPI(
    title="Agentic CRUD API",
    description="Natural Language CRUD Operations with Human-in-the-Loop",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

crud_agent = AgenticCRUDApp()

class QueryRequest(BaseModel):
    input: str
    human_verified: Optional[bool] = None

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