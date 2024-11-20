# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import uvicorn

from services.postgres import get_db, engine
from services.qdrant import get_qdrant_client, init_collection
from api.router import api_router
from core.config import SERVER_PORT
from models.product import Base
from utils.data_loader import load_products

app = FastAPI()

# Include the API router
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    """Initialize database and Qdrant collections on startup"""
    try:
        # Create database tables
        Base.metadata.create_all(bind=engine)
        
        # Load initial data if table is empty
        db = next(get_db())
        result = db.execute(text("SELECT COUNT(*) FROM products")).scalar()
        if result == 0:
            load_products(db, "datasets/product.json")
            print("Successfully loaded product data")
        db.close()
        print("Database initialization completed")

        # Initialize Qdrant collection for chat
        try:
            # Initialize collection for beauty consultations
            init_collection(
                collection_name="beauty_consultations",
                vector_size=1536  # OpenAI embeddings dimension
            )
            print("Successfully initialized Qdrant collection")
        except Exception as e:
            print(f"Error initializing Qdrant collection: {e}")
            raise e

    except Exception as e:
        print(f"Error during startup: {e}")
        raise e

@app.get("/healthz")
async def healthz(db: Session = Depends(get_db)):
    health_status = {
        "status": "healthy",
        "version": "v0.1.0",
        "services": {
            "postgres": "unhealthy",
            "qdrant": "unhealthy"
        }
    }

    try:
        # Check PostgreSQL connection
        db.execute(text("SELECT 1"))
        health_status["services"]["postgres"] = "healthy"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["services"]["postgres"] = str(e)

    try:
        # Check Qdrant connection
        qdrant_client = get_qdrant_client()
        collections = qdrant_client.get_collections()
        health_status["services"]["qdrant"] = "healthy"
        
        # Verify beauty_consultations collection exists
        if not any(col.name == "beauty_consultations" for col in collections.collections):
            health_status["status"] = "unhealthy"
            health_status["services"]["qdrant"] = "beauty_consultations collection missing"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["services"]["qdrant"] = str(e)

    if health_status["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=health_status)

    return health_status

if __name__ == "__main__":
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=SERVER_PORT,
            reload=True,
            workers=1,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
    except Exception as e:
        print(f"Error running server: {e}")