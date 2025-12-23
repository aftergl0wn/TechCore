import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collation import Collation
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.circuit_breaker import call_with_breaker, db_breaker
from app.model import Author, Book
from app.report import REPORT_SQL
from app.schema.schema import (
    AuthorSchemaRequest, BookSchemaReport, BookSchemaRequest
)


load_dotenv(".env")


class BookRepository:

    @staticmethod
    async def get_by_id(
        book_id: int,
        session: AsyncSession,
    ) -> Book:
        async def _get_by_id():
            book = await session.execute(
                select(Book).where(Book.id == book_id)
                )
            book = book.scalars().first()
            return book
        return await call_with_breaker(db_breaker, _get_by_id)

    @staticmethod
    async def create(
        new_book: BookSchemaRequest,
        session: AsyncSession,
    ) -> Book:
        async def _creat():
            new_book_data = new_book.dict()
            db_book = Book(**new_book_data)
            session.add(db_book)
            await session.commit()
            await session.refresh(db_book)
            return db_book
        return await call_with_breaker(db_breaker, _creat)

    @staticmethod
    async def get_all(session: AsyncSession,) -> list[Book]:
        async def _get_all():
            book = await session.execute(
                select(Book).options(selectinload(Book.author))
                )
            book = book.scalars().all()
            return book
        return await call_with_breaker(db_breaker, _get_all)

    @staticmethod
    async def report(session: AsyncSession,) -> list[BookSchemaReport]:
        async def _report():
            book = await session.execute(REPORT_SQL)
            book = book.mappings().all()
            return book
        return await call_with_breaker(db_breaker, _report)


class AuthorRepository:

    @staticmethod
    async def get_by_id(
        author_id: int,
        session: AsyncSession,
    ) -> Author:
        async def _get_by_id():
            author = await session.execute(
                select(Author).where(Author.id == author_id)
                )
            author = author.scalars().first()
            return author
        return await call_with_breaker(db_breaker, _get_by_id)

    @staticmethod
    async def create(
        new_author: AuthorSchemaRequest,
        session: AsyncSession,
    ) -> Author:
        async def _creat():
            new_author_data = new_author.dict()
            db_author = Author(**new_author_data)
            session.add(db_author)
            await session.commit()
            await session.refresh(db_author)
            return db_author
        return await call_with_breaker(db_breaker, _creat)


class AnalyticsRepository:
    @staticmethod
    def get_collection() -> Collation:
        client = MongoClient(os.getenv("MONGO_URL", "mongodb://mongo:27017"))
        return client["analytics"]["book_views"]

    @staticmethod
    def save_message(message: dict, collection: Collation):
        collection.insert_one(message)
