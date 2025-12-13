import asyncio

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.schema import BookSchemaUpdate
from app.deps_redis import redis_client
from app.model import Book, get_db_session
from app.routers.book import router


@pytest.fixture
def redis_mock(mocker):
    mock = mocker.AsyncMock()
    mock.get = mocker.AsyncMock(return_value=None)
    mock.set = mocker.AsyncMock()
    mock.publish = mocker.AsyncMock()
    mock.delete = mocker.AsyncMock()
    return mock


@pytest.fixture
def db_session_mock(mocker):
    mock = mocker.AsyncMock(spec=AsyncSession)
    result_mock = mocker.MagicMock()
    book = Book(id=1, title="Test Book", year=2025)
    result_mock.scalars.return_value.first.return_value = book
    mock.execute = mocker.AsyncMock(return_value=result_mock)
    mock.merge = mocker.AsyncMock(return_value=book)
    mock.add = mocker.AsyncMock()
    mock.commit = mocker.AsyncMock()
    mock.refresh = mocker.AsyncMock()
    return mock


@pytest.fixture
def app(redis_mock, db_session_mock):
    app = FastAPI()
    app.include_router(router)

    async def override_get_db_session():
        yield db_session_mock

    async def override_redis_client():
        return redis_mock

    app.dependency_overrides[get_db_session] = override_get_db_session
    app.dependency_overrides[redis_client] = override_redis_client

    return app


@pytest_asyncio.fixture
async def async_client(app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as async_client:
        yield async_client


@pytest.fixture
def book_data_new():
    return BookSchemaUpdate(title="New")


@pytest.fixture
def redis_mock_publish(redis_mock, mocker):
    pubsub_queue = asyncio.Queue()

    async def mock_publish(channel, message):
        await pubsub_queue.put({"type": "message", "data": message})

    async def mock_listen():
        while True:
            yield await pubsub_queue.get()

    redis_mock.publish = mocker.AsyncMock(side_effect=mock_publish)
    mock_pubsub = mocker.AsyncMock()
    mock_pubsub.subscribe = mocker.AsyncMock()
    mock_pubsub.listen = mock_listen
    mock_pubsub.close = mocker.AsyncMock()
    redis_mock.pubsub = mocker.MagicMock(return_value=mock_pubsub)
    redis_mock.aclose = mocker.AsyncMock()
    return redis_mock
