from sqlalchemy import select

from model import Book


def test_book_session(db_session):
    book = Book(title="New")
    db_session.add(book)
    db_session.commit()
    result = db_session.execute(select(Book))
    result = result.scalars().first()
    assert result.title == "New"
