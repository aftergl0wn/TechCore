import json
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model import Book
from app.schema.schema import BookSchemaResponse


class BookRepository:

    @staticmethod
    async def get_by_id(
        book_id: int,
        session: AsyncSession,
        redis_client: Redis,
    ) -> Book:
        cached_book = await redis_client.get(f"book:{book_id}")
        if cached_book:
            return json.loads(cached_book)
        book = await session.execute(
            select(Book).where(Book.id == book_id)
            )
        book = book.scalars().first()
        if book:
            book_data = BookSchemaResponse.from_orm(book).dict()
        else:
            book_data = None
        await redis_client.set(
            f"book:{book_id}", json.dumps(book_data)
        )
        return book
