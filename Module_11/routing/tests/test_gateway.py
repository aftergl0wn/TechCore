from fastapi.testclient import TestClient
from http import HTTPStatus

from gateway.main import app


def test_gateway_get(mock_httpx_client):
    client = TestClient(app)

    response = client.get("/api/books/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "title": "Test Book"}
    mock_httpx_client.get.assert_called_once_with(
        "http://book-service:8000/api/books/1"
    )
