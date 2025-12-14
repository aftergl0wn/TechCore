from http import HTTPStatus

import httpx
import pytest

from app.service.author_service import AuthorService


@pytest.mark.asyncio
async def test_client(retry):
    client = AuthorService("http://test")
    client.client = httpx.AsyncClient(
        base_url="http://test",
        transport=httpx.MockTransport(retry)
    )
    for _ in range(4):
        with pytest.raises(Exception):
            await client.get("/author/1")
    response = await client.get("/author/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"name": "Default Author"}
