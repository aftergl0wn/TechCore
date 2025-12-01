from http import HTTPStatus

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_root():
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == "Hello, World"
