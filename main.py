from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import uvicorn

from services.postgres import get_db, engine
from services.qdrant import get_qdrant_client
from api.router import api_router
from core.config import SERVER_PORT
from models.product import Base
from utils.data_loader import load_products

app = FastAPI()

# Include the API router
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    """Initialize database and load data on startup"""
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
        qdrant_client.get_collections()
        health_status["services"]["qdrant"] = "healthy"
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