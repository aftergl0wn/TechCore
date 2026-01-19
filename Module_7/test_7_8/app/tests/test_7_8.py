import pytest
import httpx

from http import HTTPStatus


@pytest.mark.asyncio
async def test_get_all(app, book, mocker):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.get("/api/books")
    assert response.status_code == HTTPStatus.OK
