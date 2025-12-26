
import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from http import HTTPStatus
from jose import jwt

from gateway.main import app

load_dotenv(".env")


@pytest.fixture
def mock_book_response(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = {
        "id": 1,
        "title": "Test Book",
        "year": 2020
    }
    return mock_response


@pytest.fixture
def mock_reviews_response(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = [
        {
            "_id": "review1",
            "product_id": "1",
            "rating": 5,
            "comment": "Great book"
        }
    ]
    return mock_response


@pytest.fixture
def mock_httpx_client_details(
    mocker, mock_book_response, mock_reviews_response
):
    mock_client = mocker.patch("httpx.AsyncClient")
    mock_client_instance = mocker.AsyncMock()
    mock_client.return_value.__aenter__.return_value = (
        mock_client_instance
    )

    async def get_side_effect(url):
        if "books" in url and "reviews" not in url:
            return mock_book_response
        elif "reviews" in url:
            return mock_reviews_response
        return mock_book_response

    mock_client_instance.get.side_effect = get_side_effect
    return mock_client_instance


@pytest.fixture
def auth_headers():
    payload = {"sub": "test_user", "role": "user", "exp": 9999999999}
    token = jwt.encode(
        payload,
        os.getenv("JWT_SECRET_KEY"),
        algorithm=os.getenv("JWT_ALGORITHM")
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def client():
    return TestClient(app)
