import pytest

from .book3 import Book, Ebook


@pytest.fixture
def value():
    return {
        "title": "world",
        "author": "Nik",
        "file_size": 50,
    }


def test_ebook(value):
    book = Ebook(
        title=value["title"],
        author=value["author"],
        file_size=value["file_size"]
    )
    assert book.title == value["title"]
    assert book.author == value["author"]
    assert book.file_size == value["file_size"]


def test_class(value):
    book = Ebook(
        title=value["title"],
        author=value["author"],
        file_size=value["file_size"]
    )
    assert isinstance(book, Book)
    assert issubclass(Ebook, Book)
