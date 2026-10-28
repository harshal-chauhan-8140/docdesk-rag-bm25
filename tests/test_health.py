from fastapi.testclient import TestClient

from docdesk.main import app


def test_liveness_returns_success() -> None:
    """A liveness request should succeed and return the expected JSON."""

    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == 200

    assert response.json() == {"status": "ok"}


def test_liveness_rejects_post() -> None:
    """The liveness endpoint should accept GET, not POST."""

    with TestClient(app) as client:
        response = client.post("/health/live")

    assert response.status_code == 405
