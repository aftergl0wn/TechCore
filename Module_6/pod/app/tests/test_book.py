import asyncio

import pytest
from http import HTTPStatus

from app.deps_redis import background_service_cache


@pytest.mark.asyncio
async def test_pod(
    redis_mock_publish, book_data_new, async_client, mocker
):
    mocker.patch(
        "app.deps_redis.redis_client",
        return_value=redis_mock_publish
    )
    task = asyncio.create_task(background_service_cache())
    response = await async_client.patch("/books/1", json=book_data_new)
    assert response.status_code == HTTPStatus.OK
    await asyncio.sleep(1)
    task.cancel()
    redis_mock_publish.publish.assert_called_once_with("cache:invalidate", "1")
    redis_mock_publish.delete.assert_called_once_with("book:1")
