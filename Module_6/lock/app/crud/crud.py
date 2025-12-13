import asyncio

import json
from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model import Book
from app.schema.schema import BookSchemaUpdate, BookSchemaResponse


class BookRepository:

    @staticmethod
    async def get_by_id(
        book_id: int,
        session: AsyncSession,
        redis_client: Redis,
    ) -> Book:
        cached_book = await redis_client.get(f"book:{book_id}")
        if cached_book:
            return Book(**json.loads(cached_book))
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

    @staticmethod
    async def update_book(
        db_book: Book,
        book_id: int,
        book_new: BookSchemaUpdate,
        session: AsyncSession,
        redis: Redis,
    ):
        async with redis.lock(f"inventory_lock:{book_id}", timeout=10):
            db_book = await session.merge(db_book)
            await redis.publish("cache:invalidate", str(book_id))
            obj_data = jsonable_encoder(db_book)
            update_data = book_new.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_book, field, update_data[field])
            session.add(db_book)
            await session.commit()
            await session.refresh(db_book)
            return db_book
