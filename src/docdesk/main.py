from fastapi import FastAPI

from docdesk.api.health import router as health_router

app = FastAPI(
    title="DocDesk",
    description="A documentation assistant built with retrieval-augmented generation.",
    version="0.1.0",
)

app.include_router(health_router)