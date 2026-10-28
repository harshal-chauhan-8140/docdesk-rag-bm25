from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/live")
def check_liveness() -> dict[str, str]:
    """Report that the API is running and able to answer a request."""

    return {"status": "ok"}