import time
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
    start = time.time()
    resp1, resp2 = await client.get_parallel("/author/1", "book/1")
    assert time.time() - start < 2
    assert resp1.status_code == HTTPStatus.OK
    assert resp1.json() == {"name": "test"}
    assert resp2.status_code == HTTPStatus.OK
    assert resp2.json() == {"title": "New"}
