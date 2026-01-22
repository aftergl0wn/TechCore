import structlog
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.model import Author, Book
from app.schema.schema import AuthorSchemaRequest, BookSchemaRequest


logger = structlog.get_logger()


async def book_get_by_id(
    book_id: int,
    session: AsyncSession,
) -> Optional[Book]:
    try:
        book = await session.execute(
            select(Book).where(Book.id == book_id)
            )
        book = book.scalars().first()
        return book
    except SQLAlchemyError as db_err:
        await session.rollback()
        logger.error(
            "Ошибка доступа к БД",
            book_id=book_id,
            type_error=type(db_err),
            error=str(db_err)
        )
        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail="Try again later"
        )
    except Exception as e:
        await session.rollback()
        logger.error(
            "Неизвестная ошибка",
            book_id=book_id,
            type_error=type(e),
            error=str(e)
        )
        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail="Service unavailable"
        )


async def book_create(
    new_book: BookSchemaRequest,
    session: AsyncSession,
) -> Book:
    new_book_data = new_book.dict()
    db_book = Book(**new_book_data)
    try:
        session.add(db_book)
        await session.commit()
        await session.refresh(db_book)
        return db_book
    except SQLAlchemyError as db_err:
        await session.rollback()
        logger.error(
            "Ошибка доступа к БД",
            book_data=new_book_data,
            type_error=type(db_err),
            error=str(db_err)
        )
        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail="Try again later"
        )
    except Exception as e:
        await session.rollback()
        logger.error(
            "Неизвестная ошибка",
            book_data=new_book_data,
            type_error=type(e),
            error=str(e)
        )
        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail="Service unavailable"
        )


async def author_get_by_id(
    author_id: int,
    session: AsyncSession,
) -> Optional[Author]:
    try:
        author = await session.execute(
            select(Author).where(Author.id == author_id)
            )
        author = author.scalars().first()
        return author
    except SQLAlchemyError as db_err:
        await session.rollback()
        logger.error(
            "Ошибка доступа к БД",
            author_id=author_id,
            type_error=type(db_err),
            error=str(db_err)
        )
        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail="Try again later"
        )
    except Exception as e:
        await session.rollback()
        logger.error(
            "Неизвестная ошибка",
            author_id=author_id,
            type_error=type(e),
            error=str(e)
        )
        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail="Service unavailable"
        )


async def author_create(
    new_author: AuthorSchemaRequest,
    session: AsyncSession,
) -> Author:
    new_author_data = new_author.dict()
    db_author = Author(**new_author_data)
    try:
        session.add(db_author)
        await session.commit()
        await session.refresh(db_author)
        return db_author
    except SQLAlchemyError as db_err:
        await session.rollback()
        logger.error(
            "Ошибка доступа к БД",
            author_data=new_author_data,
            type_error=type(db_err),
            error=str(db_err)
        )
        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail="Try again later"
        )
    except Exception as e:
        await session.rollback()
        logger.error(
            "Неизвестная ошибка",
            author_data=new_author_data,
            type_error=type(e),
            error=str(e)
        )
        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail="Service unavailable"
        )
