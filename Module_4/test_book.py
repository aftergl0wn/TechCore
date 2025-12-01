import pytest

from .book import BookSchema


@pytest.fixture
def data():
    return {
        "title": "War and peace",
        "year": 1867
    }


def test_book_1(data):
    book = BookSchema(
        title=data["title"],
        year=data["year"]
    )
    assert book.title == data["title"]
    assert book.year == data["year"]


def test_book_2(data):
    book = BookSchema(title=data["title"])
    assert book.title == data["title"]
    assert book.year is None
