import os

from dotenv import load_dotenv
from http import HTTPStatus
from jose import jwt


load_dotenv(".env")


def test_invalid_token(client, mock_httpx_client):
    headers = {"Authorization": "Bearer invalid_token"}

    response = client.get("/api/books/1", headers=headers)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "Invalid token" in response.json()["detail"]


def test_valid_token(client, mock_httpx_client):
    payload = {"sub": "test_user", "exp": 9999999999}
    valid_token = jwt.encode(
        payload, os.getenv("JWT_SECRET_KEY"),
        algorithm=os.getenv("JWT_ALGORITHM")
    )
    headers = {"Authorization": f"Bearer {valid_token}"}

    response = client.get("/api/books/1", headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "title": "Test Book"}
    mock_httpx_client.get.assert_called_once_with(
        "http://book-service:8000/api/books/1"
    )
