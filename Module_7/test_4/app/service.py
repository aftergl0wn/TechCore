from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import BookRepository
from app.model import Book
from app.schema import BookSchemaRequest, BookSchemaUpdate


class BookService:

    @staticmethod
    async def get_by_id(
        book_id: int,
        session: AsyncSession,
    ) -> Book:
        return await BookRepository.get_by_id(book_id, session)

    @staticmethod
    async def create(
        new_book: BookSchemaRequest,
        session: AsyncSession,
    ) -> Book:
        return await BookRepository.create(new_book, session)

    @staticmethod
    async def get_all(session: AsyncSession,) -> list[Book]:
        return await BookRepository.get_all(session)

    @staticmethod
    async def update(
        db_book: Book,
        update_book: BookSchemaUpdate,
        session: AsyncSession,
    ) -> Book:
        return await BookRepository.update(db_book, update_book, session)

    @staticmethod
    async def delete(
        db_book: Book,
        session: AsyncSession,
    ) -> bool:
        return await BookRepository.delete(db_book, session)
