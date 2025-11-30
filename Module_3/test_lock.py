import logging

import pytest

from .lock import main


@pytest.mark.asyncio
async def test_lock(caplog):
    caplog.at_level(logging.ERROR)
    await main()
    assert not caplog.text
