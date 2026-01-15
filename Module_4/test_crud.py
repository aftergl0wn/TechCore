from http import HTTPStatus

from fastapi.testclient import TestClient
import pytest

from . import crud


@pytest.fixture
def client():
    return TestClient(crud.app)


@pytest.fixture(autouse=True)
def clear_data():
    crud.id = 0
    crud.data.clear()


@pytest.fixture(autouse=True)
def value():
    return {
        "title": "War and peace",
        "year": 1867
    }


@pytest.fixture(autouse=True)
def new_value():
    return {
        "title": "New",
        "year": 1994
    }


def test_post(client, value):
    response = client.post("/books", json=value)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == value


def test_get(client, value):
    client.post("/books", json=value)
    response = client.get("/books/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == value


def test_error_get(client, value):
    response = client.get("/books/1")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Данные не найдены'}


def test_delete(client, value):
    client.post("/books", json=value)
    response = client.delete("/books/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == f"Удалена книга: {value}"


def test_update(client, value, new_value):
    client.post("/books", json=value)
    response = client.patch("/books/1", json=new_value)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == new_value
