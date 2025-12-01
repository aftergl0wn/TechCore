from typing import Optional
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Session:
    def __init__(self):
        self.data = {}
        self.id = 0


session = Session()


def get_db_session():
    yield session


class BookSchema(BaseModel):
    title: str
    year: Optional[int]


@app.post("/books")
async def create_book(
    book: BookSchema,
    db: Session = Depends(get_db_session)
):
    db.id += 1
    db.data[db.id] = book.dict()
    return db.data[db.id]


@app.get("/books/{book_id}")
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
