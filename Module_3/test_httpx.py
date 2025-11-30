import time

import pytest

from .request_httpx import main


@pytest.mark.asyncio
async def test_httpx():
    start_hundred = time.time()
    await main(100)
    result_hundred = time.time() - start_hundred
    start_one = time.time()
    await main(1)
    result_one = time.time() - start_one
    assert result_hundred < 3 * result_one
