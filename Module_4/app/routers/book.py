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
    db.id += 1
    db.data[db.id] = book.dict()
    return db.data[db.id]


@router.get("/books/{book_id}")
async def get_book(
    book_id: int,
    db: Session = Depends(get_db_session)
):
    try:
        return db.data[book_id]
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Данные не найдены"
        )
