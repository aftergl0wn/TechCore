from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud import BookRepository
from app.deps_redis import redis_client
from app.model import get_db_session
from app.schema.schema import BookSchemaResponse

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
