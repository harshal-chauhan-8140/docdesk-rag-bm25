from collections.abc import Iterator
from unittest.mock import MagicMock
import pytest

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError
from docdesk.main import app


@pytest.fixture
def api_client(
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[tuple[TestClient, MagicMock]]:
    """Provide a client with fake database settings and a controlled engine."""

    monkeypatch.setenv("DB_HOST", "test-db")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_USER", "test-user")
    monkeypatch.setenv("DB_PASSWORD", "test-only-password")
    monkeypatch.setenv("DB_NAME", "test-db")

    engine = MagicMock()

    monkeypatch.setattr(
        "docdesk.main.build_engine",
        lambda settings: engine,
    )

    with TestClient(app) as client:
        yield client, engine

    engine.dispose.assert_called_once()


def test_liveness_returns_success(api_client) -> None:
    client, engine = api_client

    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    engine.connect.assert_not_called()


def test_liveness_rejects_post(api_client) -> None:
    client, _ = api_client

    response = client.post("/health/live")

    assert response.status_code == 405


def test_readiness_queries_database(api_client) -> None:
    client, engine = api_client

    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    connection = engine.connect.return_value.__enter__.return_value

    connection.execute.assert_called_once()

    statement = connection.execute.call_args.args[0]
    assert str(statement) == "SELECT 1"


def test_readiness_handles_database_failure(api_client) -> None:
    client, engine = api_client

    engine.connect.side_effect = OperationalError(
        "SELECT 1",
        {},
        Exception("private database details"),
    )

    response = client.get("/health/ready")

    assert response.status_code == 503

    assert response.json() == {"detail": "Database unavailable"}
