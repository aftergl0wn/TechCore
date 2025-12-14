import asyncio

import httpx
import pytest

from app.service.author_service import AuthorService


@pytest.mark.asyncio
async def test_client(slow):
    client = AuthorService("http://test")
    client.client = httpx.AsyncClient(transport=httpx.MockTransport(slow))
    with pytest.raises(asyncio.TimeoutError):
        await client.get("/author/1")
