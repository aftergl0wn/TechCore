from http import HTTPStatus

from fastapi.testclient import TestClient

from main import app


def test_post():
    client = TestClient(app)
    response = client.post("/order?order_id=123")
    assert response.status_code == HTTPStatus.ACCEPTED
    assert response.json() == {"message": "Done 123"}
