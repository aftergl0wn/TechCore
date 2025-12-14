import asyncio
from http import HTTPStatus

import httpx
import pytest_asyncio


@pytest_asyncio.fixture
async def retry():
    call_count = {"count": 0}

    async def handler(request):
        call_count["count"] += 1
        if call_count["count"] < 3:
            return httpx.Response(HTTPStatus.SERVICE_UNAVAILABLE)
        return httpx.Response(HTTPStatus.OK, json={"id": 1, "name": "Alex"})
    return handler, call_count
