from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud import book_create, book_get_by_id
from app.model import get_db_session
from app.schema.schema import BookSchemaRequest, BookSchemaResponse

router = APIRouter()


@router.post(
    "/books",
    response_model=BookSchemaResponse
)
async def create_book(
    book: BookSchemaRequest,
    db: AsyncSession = Depends(get_db_session),
):
    return await book_create(book, db)


@router.get(
    "/books/{book_id}",
    response_model=BookSchemaResponse
)
async def get_book(
    book_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    book = await book_get_by_id(book_id, db)
    if book is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Book not found"
        )
    return book
