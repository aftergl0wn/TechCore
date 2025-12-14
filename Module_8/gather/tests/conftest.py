from http import HTTPStatus

import asyncio
import httpx
import pytest_asyncio


@pytest_asyncio.fixture
async def retry():

    async def handler(request):
        if "author" in str(request.url):
            await asyncio.sleep(1)
            return httpx.Response(
                status_code=HTTPStatus.OK,
                json={"name": "test"}
            )
        else:
            await asyncio.sleep(1)
            return httpx.Response(
                status_code=HTTPStatus.OK,
                json={"title": "New"}
            )

    return handler
