# api/endpoints/query.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List, Any
from pydantic import BaseModel
from services.postgres import get_db
from processors.sql_processor import SQLQueryProcessor

router = APIRouter()
sql_processor = SQLQueryProcessor()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: Optional[str] = None
    results: Optional[List[dict[str, Any]]] = None
    error: Optional[str] = None

@router.post("/query")
async def process_query(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    """Process natural language query and return results."""
    result = await sql_processor.process_query(request.query)
    if result.get("error"):
        print(f"Error occurred: {result['error']}")  # Debug logging
        return result
    return result