from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.model import Author, Book, session_maker
from app.report import REPORT_SQL
from app.schema.schema import (
    AuthorSchemaRequest, AuthorSchemaResponse,
    BookSchemaReport, BookSchemaRequest, BookSchemaResponse
)


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

    @staticmethod
    async def get_all() -> list[Book]:
        async with session_maker() as session:
            book = await session.execute(
                select(Book).options(selectinload(Book.author))
                )
            book = book.scalars().all()
        return book


    @staticmethod
    async def report() -> list[BookSchemaReport]:
        async with session_maker() as session:
            book = await session.execute(REPORT_SQL)
            book = book.mappings().all()
        return book


class AuthorRepository:

    @staticmethod
    async def get_by_id(author_id: int) -> Author:
        async with session_maker() as session:
            author = await session.execute(
                select(Author).where(Author.id == author_id)
                )
            author = author.scalars().first()
        return author

    @staticmethod
    async def create(new_author: AuthorSchemaRequest) -> Author:
        new_author_data = new_author.dict()
        db_author = Author(**new_author_data)
        async with session_maker() as session:
            session.add(db_author)
            await session.commit()
            await session.refresh(db_author)
        return db_author


class AuthorBookRepository:
    @staticmethod
    async def create(
        new_author: AuthorSchemaRequest,
        new_book: BookSchemaRequest
    ):
        new_author_data = new_author.dict()
        db_author = Author(**new_author_data)
        new_book_data = new_book.dict()
        db_book = Book(**new_book_data)
        async with session_maker() as session:
            try:
                async with session.begin():
                    session.add(db_book)
                    session.add(db_author)
                    await session.flush()
                    author_data = AuthorSchemaResponse.from_orm(db_author).dict()
                    book_data = BookSchemaResponse.from_orm(db_book).dict()
                return {"book": book_data, "author": author_data}
            except Exception as e:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=str(e)
                )
