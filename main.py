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
    # Build initial state
    initial_state = {
        "input": request.input,
        "intent": None,
        "query": None,
        "validated_query": None,
        "results": None,
        "answer": None,
        "human_verified": request.human_verified,
        "verification_required": False,
        "intermediate_steps": []
    }
    
    result = crud_agent.app.invoke(initial_state)
    
    # Check if verification is required (for CUD operations)
    if result.get("verification_required") and result.get("human_verified") is None:
        return {
            "status": "verification_required",
            "validated_query": result.get("validated_query"),
            "intent": result.get("intent")
        }
    
    # Return final result
    return {
        "status": "completed",
        "final_answer": result.get("answer"),
        "validated_query": result.get("validated_query"),
        "intent": result.get("intent")
    }