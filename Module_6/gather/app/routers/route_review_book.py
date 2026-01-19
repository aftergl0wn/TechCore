import asyncio

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_book import BookRepository
from app.database import collection
from app.deps_redis import redis_client
from app.model import get_db_session
from app.schema.schema_book_review import BookReviewSchema
from app.service import ReviewService

router_review_book = APIRouter()


@router_review_book.get(
    "/api/products/{id}/details",
    response_model=BookReviewSchema
)
async def get_book(
    id: int,
    db: AsyncSession = Depends(get_db_session),
    redis_client: Redis = Depends(redis_client),
    collection: AsyncIOMotorCollection = Depends(collection),
):
    book_task = BookRepository.get_by_id(id, db, redis_client)
    reviews_task = ReviewService.get_product_id(id, collection)
    book, reviews = await asyncio.gather(book_task, reviews_task)
    return {"book": book, "reviews": reviews}
