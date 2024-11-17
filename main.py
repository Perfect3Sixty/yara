from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import uvicorn

from services.postgres import get_db
from services.qdrant import get_qdrant_client
from api.router import api_router
from core.config import SERVER_PORT

app = FastAPI()

# Include the API router
app.include_router(api_router) 

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
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT)