from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.crud.crud import BookRepository
from app.schema.schema import (
    BookAllSchemaResponse, BookSchemaRequest, BookSchemaResponse
)

router = APIRouter()


@router.post(
    "/books",
    response_model=BookSchemaResponse
)
async def create_book(
    book: BookSchemaRequest,
):
    return await BookRepository.create(book)


@router.get(
    "/books/{book_id}",
    response_model=BookSchemaResponse
)
async def get_book(
    book_id: int,
):
    book = await BookRepository.get_by_id(book_id)
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
async def get_all_book():
    return await BookRepository.get_all()
