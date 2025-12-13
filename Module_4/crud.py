from typing import Optional
from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()
data = dict()
id = 0


class BookSchema(BaseModel):
    title: str
    year: Optional[int]


@app.post("/books")
def post(book: BookSchema):
    global id
    id += 1
    data[id] = book.dict()
    return data[id]


@app.get("/books/{book_id}")
def get(book_id: int):
    try:
        return data[book_id]
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Данные не найдены"
        )
