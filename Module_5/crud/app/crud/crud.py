from sqlalchemy import select

from app.model import Book, session_maker
from app.schema.schema import BookSchemaRequest


class BookRepository:

    @staticmethod
    async def get_by_id(book_id: int) -> Book:
        async with session_maker() as session:
            book = await session.execute(
                select(Book).where(Book.id == book_id)
                )
            book = book.scalars().first()
        return book

    @staticmethod
    async def create(new_book: BookSchemaRequest) -> Book:
        new_book_data = new_book.dict()
        db_book = Book(**new_book_data)
        async with session_maker() as session:
            session.add(db_book)
            await session.commit()
            await session.refresh(db_book)
        return db_book
