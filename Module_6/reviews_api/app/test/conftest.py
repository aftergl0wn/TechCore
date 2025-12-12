import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.database import collection
from app.router import router_review
from app.schemas import (
    ReviewRequestSchema,
    ReviewResponseSchema,
    ReviewUpdateSchema
)


@pytest.fixture
def mock_collection(mocker):
    return mocker.MagicMock()


@pytest.fixture
def app(mock_collection):
    app = FastAPI()
    app.include_router(router_review)

    async def override_collection():
        yield mock_collection

    app.dependency_overrides[collection] = override_collection
    return app


@pytest_asyncio.fixture
async def async_client(app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as async_client:
        yield async_client


@pytest.fixture
def review_request():
    return ReviewRequestSchema(
        product_id="pr1",
        rating=5,
        comment="Ok"
    )


@pytest.fixture
def review_response():
    return ReviewResponseSchema(
        id="st1",
        product_id="pr1",
        rating=5,
        comment="Ok"
    )


@pytest.fixture
def review_update():
    return ReviewUpdateSchema(
        rating=4,
    )


@pytest.fixture
def review_response_update():
    return ReviewResponseSchema(
        id="st1",
        product_id="pr1",
        rating=4,
        comment="Ok"
    )
