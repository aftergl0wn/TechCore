import httpx
import pytest
from aiobreaker import CircuitBreakerError

from app.service.author_service import AuthorService


@pytest.mark.asyncio
async def test_client(retry):
    client = AuthorService("http://test")
    client.client = httpx.AsyncClient(
        base_url="http://test",
        transport=httpx.MockTransport(retry)
    )

    for _ in range(5):
        with pytest.raises(Exception):
            await client.get("/author/1")

    with pytest.raises(CircuitBreakerError):
        await client.get("/author/1")
