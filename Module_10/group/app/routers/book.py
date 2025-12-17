import asyncio
from http import HTTPStatus

from confluent_kafka import Producer
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud import BookRepository
from app.kafka.even import send_book
from app.kafka.producer import create_producer
from app.model import get_db_session
from app.schema.schema import BookSchemaResponse

router = APIRouter()


@router.get(
    "/books/{book_id}",
    response_model=BookSchemaResponse
)
async def get_book(
    book_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db_session),
    producer: Producer = Depends(create_producer),
):
    book = await BookRepository.get_by_id(book_id, db)
    if book is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Book not found"
        )
    background_tasks.add_task(
        asyncio.to_thread,
        send_book,
        producer,
        book_id
    )
    return book
