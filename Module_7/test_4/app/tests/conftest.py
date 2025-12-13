import pytest

from app.model import Book


@pytest.fixture
def session(mocker):
    session = mocker.Mock()
    return session


@pytest.fixture
def book():
    return Book(id=1, title="New")
