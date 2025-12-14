import asyncio
from http import HTTPStatus

import httpx
import pytest_asyncio


@pytest_asyncio.fixture
async def slow():
    async def handler(request):
        await asyncio.sleep(3)
        return httpx.Response(HTTPStatus.OK, json={"id": 1, "name": "Alex"})
    return handler
