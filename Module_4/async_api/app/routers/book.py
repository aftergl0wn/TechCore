import asyncio
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app.database import Session, get_db_session
from app.schema.schema import BookSchema

router = APIRouter()


@router.post("/books")
async def create_book(
    book: BookSchema,
    db: Session = Depends(get_db_session)
):
    async with db.lock:
        db.id += 1
        db.data[db.id] = book.dict()
        await asyncio.sleep(1)
    return db.data[db.id]


@router.get("/books/{book_id}")
async def get_book(
    book_id: int,
    db: Session = Depends(get_db_session)
):
    await asyncio.sleep(1)
    try:
        return db.data[book_id]
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Данные не найдены"
        )
