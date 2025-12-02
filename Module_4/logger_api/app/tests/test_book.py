import asyncio
import logging
from http import HTTPStatus

import httpx
import pytest
import pytest_asyncio

from app.database import session
from main import app


@pytest_asyncio.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        yield client


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


@pytest.mark.asyncio
async def test_post(client, value, caplog):
    with caplog.at_level(logging.INFO):
        answer = await asyncio.gather(
            *[client.post("/books", json=value) for _ in range(1000)]
        )
    assert "Время выполнения" in caplog.text
    for response in answer:
        assert response.status_code == HTTPStatus.OK
        assert response.json() == value


@pytest.mark.asyncio
async def test_get(client, value, caplog):
    with caplog.at_level(logging.INFO):
        await asyncio.gather(
            *[client.post("/books", json=value) for _ in range(1000)]
        )
        answer = await asyncio.gather(
            *[client.get(f"/books/{i}") for i in range(1, 1001)]
        )
    assert "Время выполнения" in caplog.text
    for response in answer:
        assert response.status_code == HTTPStatus.OK
        assert response.json() == value


@pytest.mark.asyncio
async def test_error_get(client, caplog):
    with caplog.at_level(logging.INFO):
        response = await client.get("/books/1")
    assert "Время выполнения" in caplog.text
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found'}
