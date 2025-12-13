import pytest
from fastapi import FastAPI

from app.book import router
from app.model import Book, get_db_session


@pytest.fixture
def book():
    return Book(id=1, title="New")


@pytest.fixture
def session(book, mocker):
    session = mocker.AsyncMock()
    session.commit = mocker.AsyncMock()
    session.refresh = mocker.AsyncMock()
    session.add = mocker.MagicMock()
    return session


@pytest.fixture
def app(session, mocker):
    app = FastAPI()
    app.include_router(router, prefix="/api")

    async def override_get_db_session():
        yield session

    app.dependency_overrides[get_db_session] = override_get_db_session

    return app
