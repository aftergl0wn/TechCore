import time

import pytest

from .async_gather import main


@pytest.mark.asyncio
async def test_async_gather():
    start = time.time()
    await main()
    assert time.time() - start < 4
