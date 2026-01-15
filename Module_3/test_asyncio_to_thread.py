import time

import pytest

from .asyncio_to_thread import main


@pytest.mark.asyncio
async def test_main():
    start = time.time()
    result = await main()
    assert 5 <= time.time() - start < 6
    assert result == ['End work old_func', [0, 1, 2, 3, 4]]
