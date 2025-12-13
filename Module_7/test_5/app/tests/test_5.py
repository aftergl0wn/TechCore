from http import HTTPStatus
from fastapi.testclient import TestClient


def test_get_all(app, book, mocker):
    client = TestClient(app)
    response = client.get("/api/books")
    assert response.status_code == HTTPStatus.OK
