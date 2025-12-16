import asyncio
import json
from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_get_book_sends_kafka_event(async_client, mock_producer):
    response = await async_client.get("/books/1")

    assert response.status_code == HTTPStatus.OK

    await asyncio.sleep(0.5)

    call_args = mock_producer.produce.call_args
    assert call_args[0][0] == "book_views"
    assert json.loads(call_args[1]["value"].decode("utf-8")) == {"book_id": 1}
