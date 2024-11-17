from fastapi import APIRouter
from api.endpoints import search

api_router = APIRouter()

# Include routes from endpoints
api_router.include_router(search.router, tags=["search"])