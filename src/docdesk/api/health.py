import logging

from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/health", tags=["health"])

logger = logging.getLogger(__name__)


@router.get("/live")
def check_liveness() -> dict[str, str]:
    """Check that the API can respond without requiring PostgreSQL."""

    return {"status": "ok"}


@router.get("/ready")
def check_readiness(request: Request) -> dict[str, str]:
    """Check that the API can execute a query against PostgreSQL."""

    try:
        with request.app.state.engine.connect() as connection:
            connection.execute(text("SELECT 1"))

    except SQLAlchemyError:
        logger.warning("Database readiness check failed")

        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        ) from None

    return {"status": "ok"}
