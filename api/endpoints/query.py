# api/endpoints/query.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List, Any, Dict
from pydantic import BaseModel
from services.postgres import get_db
from processors.sql_processor import SQLQueryProcessor
from processors.txt2sql_processor import Txt2sqlProcessor
import pandas as pd
from fastapi.responses import JSONResponse


router = APIRouter()
sql_processor = SQLQueryProcessor()
txt2sql_processor = Txt2sqlProcessor()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    results: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None

@router.post("/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    """Process natural language query and return results."""
    result = await sql_processor.process_query(request.query)
    if result.get("error"):
        print(f"Error occurred: {result['error']}")  # Debug logging
        return result

@router.post("/v1/query", response_model=QueryResponse)
async def process_natural_query(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    """Process natural language query using PremSQL agent and return results."""
    try:
        # Execute the query through PremSQL agent
        agent_response = txt2sql_processor.agent(request.query)
        
        if agent_response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No results found for the given query"
            )
        
        # Get the DataFrame from the agent's response
        df = agent_response.show_output_dataframe()
        
        if df is None or df.empty:
            return QueryResponse(
                query=request.query,
                results=[],
                error=None
            )
        
        # Convert DataFrame to list of dictionaries
        results = df.to_dict(orient='records')
        
        # Clean up the results - handle non-JSON serializable objects
        cleaned_results = []
        for item in results:
            cleaned_item = {}
            for key, value in item.items():
                # Handle non-serializable types
                if pd.isna(value):
                    cleaned_item[key] = None
                elif isinstance(value, pd.Timestamp):
                    cleaned_item[key] = value.isoformat()
                else:
                    cleaned_item[key] = value
            cleaned_results.append(cleaned_item)
        
        return QueryResponse(
            query=request.query,
            results=cleaned_results,
            error=None
        )
        
    except Exception as e:
        # Log the error for debugging
        print(f"Error processing query: {str(e)}")
        
        # Return a structured error response
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=QueryResponse(
                query=request.query,
                results=None,
                error=f"Error processing query: {str(e)}"
            ).dict()
        )