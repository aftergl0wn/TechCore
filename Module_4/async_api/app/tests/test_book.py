import asyncio
import time
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
async def test_post(client, value):
    start = time.time()
    answer = await asyncio.gather(
        *[client.post("/books", json=value) for _ in range(1000)]
    )
    assert time.time() - start < 2
    for response in answer:
        assert response.status_code == HTTPStatus.OK
        assert response.json() == value


@pytest.mark.asyncio
async def test_get(client, value):
    start = time.time()
    await asyncio.gather(
        *[client.post("/books", json=value) for _ in range(1000)]
    )
    answer = await asyncio.gather(
        *[client.get(f"/books/{i}") for i in range(1, 1001)]
    )
    assert time.time() - start < 4
    for response in answer:
        assert response.status_code == HTTPStatus.OK
        assert response.json() == value
