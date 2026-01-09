import asyncio

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.database import collection
from app.deps_redis import redis_client
from app.model import get_db_session
from app.routers.route_review_book import router_review_book
from app.schema.schema_book_review import BookSchemaResponse
from app.schema.schema_review import ReviewResponseSchema


@pytest.fixture
def mock_collection(mocker):
    return mocker.MagicMock()


@pytest.fixture
def mock_redis(mocker):
    return mocker.MagicMock()


@pytest.fixture
def mock_db_session(mocker):
    return mocker.MagicMock()


@pytest.fixture
def app(mock_collection, mock_db_session, mock_redis):
    app = FastAPI()
    app.include_router(router_review_book)

    async def override_collection():
        yield mock_collection

    async def override_db():
        yield mock_collection

    async def override_redis():
        yield mock_redis

    app.dependency_overrides[collection] = override_collection
    app.dependency_overrides[get_db_session] = override_db
    app.dependency_overrides[redis_client] = override_redis
    return app


@pytest_asyncio.fixture
async def async_client(app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as async_client:
        yield async_client


@pytest.fixture
def review_response():
    return ReviewResponseSchema(
        id="st1",
        product_id=1,
        rating=5,
        comment="Ok"
    )


@pytest.fixture
def book_response():
    return BookSchemaResponse(
        id=1,
        title="Book",
        year=1995
    )


@pytest_asyncio.fixture
async def delay_book(book_response):
    await asyncio.sleep(1)
    return book_response


@pytest_asyncio.fixture
async def delay_review(review_response):
    await asyncio.sleep(1)
    return [review_response]
