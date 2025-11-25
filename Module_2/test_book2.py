import pytest

from .book2 import Book


@pytest.fixture
def value():
    return {"title": "world", "author": "Nik"}


@pytest.fixture
def value2():
    return {"title": "home", "author": "Tom"}


def test_repr_book(value, capsys):
    book = Book(title=value["title"], author=value["author"])
    print(book)
    captured = capsys.readouterr()
    assert (
        f"Book(author={value['author']}, title={value['title']})"
        in captured.out
    )


def test_eq_book(value, value2):
    book1 = Book(title=value["title"], author=value["author"])
    book2 = Book(title=value["title"], author=value["author"])
    book3 = Book(title=value2["title"], author=value2["author"])
    assert book1 == book2
    assert book1 != book3
