from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud import AuthorBookRepository
from app.model import get_db_session
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
    session: AsyncSession = Depends(get_db_session),
):
    return await AuthorBookRepository.create(author, book, session)
