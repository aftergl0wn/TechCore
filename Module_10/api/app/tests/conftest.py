import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.kafka.producer import create_producer
from app.model import Book, get_db_session
from app.routers.book import router


@pytest.fixture
def session(mocker):
    session = mocker.AsyncMock()
    book = Book(id=1, title="War and peace", year=1867)
    scalars_mock = mocker.MagicMock()
    scalars_mock.first.return_value = book
    result = mocker.MagicMock()
    result.scalars.return_value = scalars_mock
    session.execute = mocker.AsyncMock(return_value=result)
    return session


@pytest.fixture
def app(session, mocker):

    app = FastAPI()
    app.include_router(router)

    async def override_get_db_session():
        yield session

    mock_producer = mocker.MagicMock()

    def override_create_producer():
        return mock_producer

    app.dependency_overrides[get_db_session] = override_get_db_session
    app.dependency_overrides[create_producer] = override_create_producer
    app.state.mock_producer = mock_producer

    return app


@pytest_asyncio.fixture
async def async_client(app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
def mock_producer(app):
    return app.state.mock_producer
