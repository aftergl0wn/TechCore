from http import HTTPStatus
from fastapi.testclient import TestClient


def test_post(app, mocker):
    client = TestClient(app)
    response = client.post("/api/books", json={"title": 123})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
