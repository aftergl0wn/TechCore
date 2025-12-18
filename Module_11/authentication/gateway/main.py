import httpx
from fastapi import Depends, FastAPI, Response

from .security.jwt import verify_token

app = FastAPI(title="Gateway")


@app.get("/api/books/{id}")
async def gateway_get(
    id: int,
    token: dict = Depends(verify_token)
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
