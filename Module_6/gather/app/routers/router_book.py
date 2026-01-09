from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_book import BookRepository
from app.deps_redis import redis_client
from app.model import get_db_session
from app.schema.schema_book_author import BookSchemaResponse, BookSchemaUpdate

router = APIRouter()


@router.get(
    "/books/{book_id}",
    response_model=BookSchemaResponse
)
async def get_book(
    book_id: int,
    db: AsyncSession = Depends(get_db_session),
    redis_client: Redis = Depends(redis_client),
):
    book = await BookRepository.get_by_id(book_id, db, redis_client)
    if book is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Book not found"
        )
    return book


@router.patch(
    "/books/{book_id}",
    response_model=BookSchemaResponse
)
async def partially_update_book(
    book_id: int,
    book: BookSchemaUpdate,
    db: AsyncSession = Depends(get_db_session),
    redis_client: Redis = Depends(redis_client),
):
    db_book = await BookRepository.get_by_id(book_id, db, redis_client)
    if db_book is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Book not found"
        )
    update_book = await BookRepository.update_book(
        db_book,
        book_id,
        book,
        db,
        redis_client
    )
    return update_book
