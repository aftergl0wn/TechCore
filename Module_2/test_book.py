import pytest

from .book import Book


@pytest.fixture
def value():
    return {
        "title": "world",
        "author": "Nik"
    }


def test_book(value):
    book = Book(
        title=value["title"],
        author=value["author"]
    )
    assert book.title == value["title"]
    assert book.author == value["author"]
