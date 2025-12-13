from app.model import Book

import pytest


@pytest.fixture
def session(mocker):
    session = mocker.Mock()
    return session


@pytest.fixture
def book():
    return Book(id=1, title="New")


@pytest.fixture
def book_old():
    return Book(id=1, title="old")


@pytest.fixture
def book_schema(mocker):
    return mocker.Mock()
