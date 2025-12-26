import asyncio

import httpx
from fastapi import Depends, FastAPI, HTTPException, Response
from http import HTTPStatus

from .security.jwt import require_role

app = FastAPI(title="Gateway")


@app.get("/api/books/{id}")
async def gateway_get(
    id: int,
    token: dict = Depends(require_role("user"))
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://book-service:8000/api/books/{id}"
        )
    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=response.headers.get("content-type"),
    )


@app.get("/api/details/{id}")
async def get_details(
    id: int,
    token: dict = Depends(require_role("user"))
):
    async def fetch_book():
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://book-service:8000/api/books/{id}"
            )
            if response.status_code == HTTPStatus.OK:
                return response.json()
            return None

    async def fetch_reviews():
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://book-service:8000/api/products/{id}/reviews"
            )
            if response.status_code == HTTPStatus.OK:
                return response.json()
            return []

    book_data, reviews_data = await asyncio.gather(
        fetch_book(),
        fetch_reviews()
    )

    if book_data is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Book not found"
        )

    return {
        "book": book_data,
        "reviews": reviews_data
    }
