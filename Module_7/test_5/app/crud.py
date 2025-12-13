from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.model import Book
from app.schema import BookSchemaRequest, BookSchemaUpdate


class BookRepository:

    @staticmethod
    async def get_by_id(
        book_id: int,
        session: AsyncSession,
    ) -> Book:
        book = await session.execute(
            select(Book).where(Book.id == book_id)
            )
        book = book.scalars().first()
        return book

    @staticmethod
    async def create(
        new_book: BookSchemaRequest,
        session: AsyncSession,
    ) -> Book:
        new_book_data = new_book.dict()
        db_book = Book(**new_book_data)
        session.add(db_book)
        await session.commit()
        await session.refresh(db_book)
        return db_book

    @staticmethod
    async def get_all(session: AsyncSession,) -> list[Book]:
        book = await session.execute(
            select(Book).options(selectinload(Book.author))
            )
        book = book.scalars().all()
        return book

    @staticmethod
    async def update(
        db_book: Book,
        update_book: BookSchemaUpdate,
        session: AsyncSession,
    ) -> Book:
        obj_data = jsonable_encoder(db_book)
        update_data = update_book.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_book, field, update_data[field])
        session.add(db_book)
        await session.commit()
        await session.refresh(db_book)
        return db_book

    @staticmethod
    async def delete(
        db_book: Book,
        session: AsyncSession,
    ) -> bool:
        await session.delete(db_book)
        await session.commit()
        return True
