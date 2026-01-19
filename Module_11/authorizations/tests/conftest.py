from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from gateway.main import app


@pytest.fixture
def mock_httpx_response(mocker):
    mock_response = mocker.AsyncMock()
    mock_response.content = b'{"id": 1, "title": "Test Book"}'
    mock_response.status_code = HTTPStatus.OK
    mock_response.headers = {"content-type": "application/json"}
    return mock_response


@pytest.fixture
def mock_httpx_client(mocker, mock_httpx_response):
    mock_client = mocker.patch("httpx.AsyncClient")
    mock_client_instance = mocker.AsyncMock()
    mock_client.return_value.__aenter__.return_value = (
        mock_client_instance
    )
    mock_client_instance.get.return_value = mock_httpx_response
    return mock_client_instance


@pytest.fixture
def client():
    return TestClient(app)
