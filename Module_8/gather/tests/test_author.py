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
    task1, task2 = await client.get_parallel("/author-service", "/review-service")
    assert time.time() - start < 2
    assert task1.status_code == HTTPStatus.OK
    assert task1.json() == {"name": "test"}
    assert task2.status_code == HTTPStatus.OK
    assert task2.json() == {"title": "New"}
