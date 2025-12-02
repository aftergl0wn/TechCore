from http import HTTPStatus

from fastapi.testclient import TestClient
import pytest

from .di import app, session


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def value():
    return {
        "title": "War and peace",
        "year": 1867
    }


@pytest.fixture(autouse=True)
def clear_db():
    session.data.clear()
    session.id = 0


def test_post(client, value):
    response = client.post("/books", json=value)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == value


def test_get(client, value):
    client.post("/books", json=value)
    response = client.get("/books/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == value


def test_error_get(client):
    response = client.get("/books/1")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Данные не найдены'}
