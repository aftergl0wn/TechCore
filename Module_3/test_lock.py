import time

import pytest

from .lock import main


@pytest.mark.asyncio
async def test_lock(mocker):
    mocker_lock = mocker.MagicMock()
    with mocker.patch("asyncio.Lock", return_value=mocker_lock):
        result = await main()
    assert result == ["data" for _ in range(10)]
    assert mocker_lock.__aenter__.call_count == 10


@pytest.mark.asyncio
async def test_lock_time():
    start = time.time()
    await main()
    assert time.time() - start >= 10
