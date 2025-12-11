from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps_redis import redis_client
from app.model import Book, get_db_session
from app.routers.book import router


@pytest.fixture
def redis_mock():
    mock = AsyncMock()
    mock.get = AsyncMock()
    mock.set = AsyncMock()
    return mock


@pytest.fixture
def db_session_mock():
    mock = AsyncMock(spec=AsyncSession)
    result_mock = MagicMock()
    book = Book(id=1, title="Test Book", year=2025)
    result_mock.scalars.return_value.first.return_value = book
    mock.execute = AsyncMock(return_value=result_mock)
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
def book_data():
    return {
        "id": 1,
        "title": "Test Book",
        "year": 2025
    }
