import pytest
from http import HTTPStatus

from app.service.author_service import AuthorService


@pytest.mark.asyncio
async def test_session_get_works(test_server):
    service = AuthorService(base_url=str(test_server.make_url("")))
    response = await service.get("/test")
    assert response.status == HTTPStatus.OK
    await response.json() == {"name": "Tom"}
