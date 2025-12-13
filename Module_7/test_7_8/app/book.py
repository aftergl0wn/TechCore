from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.model import get_db_session
from app.schema import (
    BookAllSchemaResponse,
    BookSchemaRequest, BookSchemaResponse, BookSchemaUpdate
)
from app.service import BookService


router = APIRouter()


@router.post(
    "/books",
    response_model=BookSchemaResponse
)
async def create_book(
    book: BookSchemaRequest,
    db: AsyncSession = Depends(get_db_session),
):
    return await BookService.create(book, db)


@router.get(
    "/books/{book_id}",
    response_model=BookSchemaResponse
)
async def get_book(
    book_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    book = await BookService.get_by_id(book_id, db)
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
    return await BookService.get_all(db)


@router.patch(
    "/books/{book_id}",
    response_model=BookSchemaResponse
)
async def put_book(
    book_id: int,
    obj_in: BookSchemaUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    book = await BookService.get_by_id(book_id, db)
    if book is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Book not found"
        )
    book_update = await BookService.update(book, obj_in, db)
    return book_update


@router.delete(
    "/books/{book_id}",
    response_model=BookSchemaResponse
)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    book = await BookService.get_by_id(book_id, db)
    if book is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Book not found"
        )
    book = await BookService.delete(book, db)
    return book
