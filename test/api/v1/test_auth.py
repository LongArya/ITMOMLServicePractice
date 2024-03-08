from sqlmodel import Session
from fastapi.testclient import TestClient
from .utils import client_fixture, session_fixture
from backend.core.config import settings


def test_register(client_fixture: TestClient) -> None:
    register_endpoint = f"{settings.API_V1_STR}/auth/register"
    response = client_fixture.post(
        register_endpoint,
        json={
            "name": "test_name",
            "email": "test_email.one@gmail.com",
            "is_active": False,
            "is_superuser": False,
            "password": "pwd",
        },
    )
    data = response.json()

    assert response.status_code == 200, f"{data}"
    assert data["name"] == "test_name"
    assert data["email"] == "test_email.one@gmail.com"
    assert data["is_active"] is False
    assert data["is_superuser"] is False
