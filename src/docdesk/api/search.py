import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Request
from sqlalchemy.exc import SQLAlchemyError

from docdesk.retrieval import search_chunks

router = APIRouter(tags=["search"])
logger = logging.getLogger(__name__)


@router.get("/search")
def search(
    request: Request,
    q: Annotated[str, Query(min_length=1, max_length=500)],
    limit: Annotated[int, Query(ge=1, le=10)] = 5,
) -> dict:
    """Search indexed documentation and return source passages."""

    if not q.strip():
        raise HTTPException(status_code=422, detail="Query must not be blank")

    try:
        results = search_chunks(request.app.state.engine, q, limit)
    except SQLAlchemyError:
        logger.warning("Database unavailable during search")
        raise HTTPException(
            status_code=503,
            detail="Search temporarily unavailable",
        ) from None

    return {"query": q, "results": results}
