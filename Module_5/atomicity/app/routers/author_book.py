from fastapi import APIRouter

from app.crud.crud import AuthorBookRepository
from app.schema.schema import (
    AuthorSchemaRequest, AuthorBookSchemaResponse, BookSchemaRequest
)

router_author_book = APIRouter()


@router_author_book.post(
    "/author_book",
    response_model=AuthorBookSchemaResponse
)
async def create_author_book(
    author: AuthorSchemaRequest,
    book: BookSchemaRequest,
):
    return await AuthorBookRepository.create(author, book)
