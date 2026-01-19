import httpx
import pytest

from app.service.author_service import AuthorService


@pytest.mark.asyncio
async def test_client():
    base_url = "http://test"
    client = AuthorService(base_url)
    assert isinstance(client.client, httpx.AsyncClient)
    assert client.client.base_url == base_url
