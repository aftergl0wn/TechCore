import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .model import Author, Base, Book


@pytest.fixture
def book_data():
    return {"title": "Winter", "year": 2000}


@pytest.fixture
def author_data():
    return {
        "name": "Tom",
    }


@pytest.fixture
def session():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()
    Base.metadata.drop_all(engine)


def test_book(book_data, session):
    book = Book(title=book_data["title"], year=book_data["year"])
    session.add(book)
    session.commit()
    result = session.query(Book).first()
    assert result.title == book_data["title"]
    assert result.year == book_data["year"]


def test_author(author_data, session):
    author = Author(name=author_data["name"])
    session.add(author)
    session.commit()
    result = session.query(Author).first()
    assert result.name == author_data["name"]
