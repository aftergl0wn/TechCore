import logging
import time

import pytest

from .wait import wait


@pytest.mark.asyncio
async def test_wait(caplog):
    start = time.time()
    with pytest.raises(TimeoutError):
        await wait()
    delta = time.time() - start
    assert "Лимит времени исчерпан" in caplog.text
    assert 1 < delta < 3
