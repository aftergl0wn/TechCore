from http import HTTPStatus

import asyncio
import httpx
import pytest_asyncio


@pytest_asyncio.fixture
async def retry():
    count = {
        "max": 0,
        "active": 0
    }

    async def handler(request):
        nonlocal count
        count["active"] += 1
        count["max"] = max(count["max"], count["active"])
        await asyncio.sleep(1)
        count["active"] -= 1
        return httpx.Response(HTTPStatus.OK, json={"name": "test"})
    return handler, count
