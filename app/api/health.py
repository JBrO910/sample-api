from fastapi import APIRouter, Depends, Query, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import get_db
from app.utils.rate_limiter import rate_limiter
from app.core.logging import logger

router = APIRouter()


@router.get("/api/health")
def health_check(
    request: Request,
    query: str | None = Query(None),
    db: Session = Depends(get_db),
    _: None = Depends(rate_limiter),
):
    """
    Health check endpoint with logging.
    """

    client_ip = request.client.host
    logger.info(f"Incoming request from {client_ip} with query={query}")

    # Check DB connection
    try:
        db.execute(text("SELECT 1"))
        db_connected = True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        db_connected = False

    # Check if table has data
    has_data = False
    try:
        result = db.execute(text("SELECT COUNT(*) FROM task"))
        count = result.scalar()
        has_data = count > 0
    except Exception as e:
        logger.error(f"Failed to query task table: {e}")
        has_data = False

    # Filtering logic
    if query:
        if query == "database":
            return {"db_connected": db_connected}
        elif query == "data":
            return {"has_data": has_data}
        else:
            logger.warning(f"Invalid query parameter from {client_ip}: {query}")
            raise HTTPException(status_code=400, detail="Invalid query parameter")

    return {
        "db_connected": db_connected,
        "has_data": has_data,
    }