from typing import Union
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.postgres import get_db
from services.qdrant import get_qdrant_client

router = APIRouter()

# Initialize Qdrant client
qdrant_client = get_qdrant_client()

@router.get("/items/{item_id}")
def read_item(
    item_id: int, 
    q: Union[str, None] = None, 
    db: Session = Depends(get_db)
):
    # Here you can use both db and qdrant_client
    return {"item_id": item_id, "q": q}

@router.get("/search/{query}")
async def search(
    query: str,
    db: Session = Depends(get_db)
):
    # Example of using both services
    # PostgreSQL query
    # db_results = db.execute("SELECT * FROM your_table WHERE...")
    
    # Qdrant search
    # vector_results = qdrant_client.search(
    #     collection_name="your_collection",
    #     query_vector=[...],
    #     limit=10
    # )
    
    return {"query": query, "results": "example"}