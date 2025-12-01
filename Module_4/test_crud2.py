from http import HTTPStatus

from fastapi.testclient import TestClient
import pytest

from . import crud2


@pytest.fixture
def client():
    return TestClient(crud2.app)


@pytest.fixture(autouse=True)
def clear_data():
    crud2.id = 0
    crud2.data.clear()


@pytest.fixture
def value():
    return {
        "title": "War and peace",
        "year": "abc"
    }


def test_err_post(client, value):
    response = client.post("/books", json=value)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {
                                "detail": [
                                    {
                                        "loc": [
                                            "body",
                                            "year"
                                        ],
                                        "msg": "value is not a valid integer",
                                        "type": "type_error.integer"
                                    }
                                ]
                            }
