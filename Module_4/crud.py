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


class BookSchemaUpdate(BookSchema):
    title: Optional[str]


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


@app.delete("/books/{book_id}")
def delete(book_id: int):
    book = get(book_id)
    del data[book_id]
    return f"Удалена книга: {book}"


@app.patch("/books/{book_id}")
def update(book_id: int, update_book: BookSchemaUpdate):
    book = get(book_id)
    update_dict = update_book.dict(exclude_unset=True)
    for key in book:
        if key in update_dict:
            book[key] = update_dict[key]
    return book
