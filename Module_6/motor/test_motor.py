import pytest

from .main import ping


@pytest.mark.asyncio
async def test_ping():
    response = await ping()
    assert response == {"ok": 1}
