from http import HTTPStatus

import httpx
import pytest_asyncio


@pytest_asyncio.fixture
async def retry():
    async def handler(request):
        return httpx.Response(HTTPStatus.SERVICE_UNAVAILABLE)
    return handler
