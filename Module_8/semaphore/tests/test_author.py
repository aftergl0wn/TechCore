import asyncio
import httpx
import pytest

from app.service.author_service import AuthorService


@pytest.mark.asyncio
async def test_client(retry):
    handler, count = retry
    client = AuthorService("http://test")
    client.client = httpx.AsyncClient(
        base_url="http://test",
        transport=httpx.MockTransport(handler)
    )
    await asyncio.gather(*[client.get("/author/1") for _ in range(10)])
    assert count["max"] <= 5
