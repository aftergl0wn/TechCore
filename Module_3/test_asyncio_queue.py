import pytest

from .asyncio_queue import main


@pytest.fixture
def data():
    return [i for i in range(5)]


@pytest.mark.asyncio
async def test_queue(data):
    result = await main(data)
    assert data == result
