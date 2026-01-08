import inspect

import pytest

from app.kafka.analytics_worker import consume_messages


@pytest.mark.asyncio
async def test_loop():
    source = inspect.getsource(consume_messages)
    assert 'subscribe(["book_views"])' in source
    assert 'poll(1.0)' in source
