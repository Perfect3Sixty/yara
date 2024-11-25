from fastapi import APIRouter
from api.endpoints import search, query, chat

api_router = APIRouter(prefix="/api")

# Include routes from endpoints
api_router.include_router(search.router, tags=["search"])
# api_router.include_router(query.router, tags=["query"])
api_router.include_router(chat.router, tags=["chat"])
