import asyncio
from http import HTTPStatus

import structlog
from confluent_kafka import Producer
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud import BookRepository
from app.kafka.even import send_book
from app.kafka.producer import create_producer
from app.model import get_db_session
from app.schema.schema import (
    BookAllSchemaResponse, BookSchemaRequest, BookSchemaResponse
)
from app.tracing import get_book_counter

logger = structlog.get_logger(__name__)
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
    logger.info("get_book", book_id=book_id)
    book = await BookRepository.get_by_id(book_id, db)
    if book is None:
        logger.warning("book_not_found", book_id=book_id)
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Book not found"
        )
    logger.info("book_found", book_id=book_id, title=book.title)
    background_tasks.add_task(
        asyncio.to_thread,
        send_book,
        producer,
        book_id
    )
    return book


@router.post(
    "/book",
    response_model=BookSchemaResponse,
    status_code=HTTPStatus.CREATED
)
async def create_book(
    book: BookSchemaRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db_session),
    producer: Producer = Depends(create_producer),
):
    logger.info("creat_book_start")
    new_book = await BookRepository.create(book, db)
    logger.info("book_created", book_id=new_book.id, title=new_book.title)
    book_count = get_book_counter()
    book_count.add(1)
    background_tasks.add_task(
        asyncio.to_thread,
        send_book,
        producer,
        new_book.id
    )
    return new_book


@router.get(
    "/books",
    response_model=list[BookAllSchemaResponse]
)
async def get_all_book(
    db: AsyncSession = Depends(get_db_session),
):

    return await BookRepository.get_all(db)
