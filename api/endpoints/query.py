# api/endpoints/query.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from services.postgres import get_db
from processors.sql_processor import SQLQueryProcessor

router = APIRouter()
sql_processor = SQLQueryProcessor()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: Optional[str]
    results: Optional[list]
    error: Optional[str]

@router.post("/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    """Process natural language query and return results."""
    try:
        result = await sql_processor.process_query(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

