import os

from dotenv import load_dotenv
from http import HTTPStatus
from jose import jwt


load_dotenv(".env")


def test_role_missing_in_token(client, mock_httpx_client):
    payload = {"sub": "test_user", "exp": 9999999999}
    token = jwt.encode(
        payload,
        os.getenv("JWT_SECRET_KEY"),
        algorithm=os.getenv("JWT_ALGORITHM")
    )
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/books/1", headers=headers)

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert "role or scope not found" in response.json()["detail"]


def test_role_wrong_role(client, mock_httpx_client):
    payload = {"sub": "test_user", "role": "non", "exp": 9999999999}
    token = jwt.encode(
        payload,
        os.getenv("JWT_SECRET_KEY"),
        algorithm=os.getenv("JWT_ALGORITHM")
    )
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/books/1", headers=headers)

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert "Required role 'user' not found" in response.json()["detail"]


def test_correct_role(client, mock_httpx_client):
    payload = {"sub": "test_user", "role": "user", "exp": 9999999999}
    token = jwt.encode(
        payload,
        os.getenv("JWT_SECRET_KEY"),
        algorithm=os.getenv("JWT_ALGORITHM")
    )
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/books/1", headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "title": "Test Book"}
    mock_httpx_client.get.assert_called_once_with(
        "http://book-service:8000/api/books/1"
    )
