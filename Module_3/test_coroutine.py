import time

import pytest

from .coroutine import main


@pytest.mark.asyncio
async def test_coroutine():
    start = time.time()
    result = await main()
    assert time.time() - start < 2
    assert result == "Done"
