import json
import pytest


@pytest.mark.asyncio
async def test_redis(
    app, redis_mock, db_session_mock, book_data, async_client, mocker
):
    redis_mock.get = mocker.AsyncMock(
        side_effect=[None, json.dumps(book_data)]
    )
    response1 = await async_client.get("/books/1")
    assert response1.status_code == 200
    assert db_session_mock.execute.call_count == 1
    response2 = await async_client.get("/books/1")
    assert response2.status_code == 200
    assert db_session_mock.execute.call_count == 1
