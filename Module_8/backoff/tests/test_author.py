from http import HTTPStatus

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
    response = await client.get("/author/1")
    assert count["count"] == 3
    assert response.status_code == HTTPStatus.OK
