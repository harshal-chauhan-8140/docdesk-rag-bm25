from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from docdesk.api.health import router as health_router
from docdesk.api.search import router as search_router
from docdesk.config import Settings
from docdesk.database import build_engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Create shared resources on startup and release them on shutdown."""

    settings = Settings()

    app.state.engine = build_engine(settings)

    try:
        yield
    finally:
        app.state.engine.dispose()


app = FastAPI(
    title="DocDesk",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(search_router)
