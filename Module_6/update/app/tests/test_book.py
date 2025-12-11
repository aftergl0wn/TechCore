from unittest.mock import AsyncMock

import pytest


@pytest.mark.asyncio
async def test_redis(
    app, redis_mock, db_session_mock, book_data_new, async_client
):
    redis_mock.get = AsyncMock(side_effect=[None])
    redis_mock.delete = AsyncMock(side_effect=[None])
    response = await async_client.patch("/books/1", json=book_data_new)
    assert response.status_code == 200
    redis_mock.delete.assert_awaited_once_with("book:1")
