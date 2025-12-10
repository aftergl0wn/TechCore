from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud import BookRepository
from app.model import get_db_session
from app.schema.schema import (
    BookAllSchemaResponse, BookSchemaReport,
    BookSchemaRequest, BookSchemaResponse
)

router = APIRouter()


@router.post(
    "/books",
    response_model=BookSchemaResponse
)
async def create_book(
    book: BookSchemaRequest,
    db: AsyncSession = Depends(get_db_session),
):
    return await BookRepository.create(book, db)


@router.get(
    "/books/{book_id}",
    response_model=BookSchemaResponse
)
async def get_book(
    book_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    book = await BookRepository.get_by_id(book_id, db)
    if book is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Book not found"
        )
    return book


@router.get(
    "/books",
    response_model=list[BookAllSchemaResponse]
)
async def get_all_book(
    db: AsyncSession = Depends(get_db_session),
):
    return await BookRepository.get_all(db)


@router.get(
    "/books_report",
    response_model=list[BookSchemaReport]
)
async def report(
    db: AsyncSession = Depends(get_db_session),
):
    return await BookRepository.report(db)
