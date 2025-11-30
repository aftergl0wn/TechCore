import pytest

from .i_o_aiofiles import read_file, write_file


@pytest.fixture
def dict_value():
    return {
        "name": "Алиса",
        "year": 2020,
        "message": "Hi",
    }


@pytest.fixture
def file_name():
    return "config.json"


@pytest.mark.asyncio
async def test_write_file(dict_value, file_name, tmp_path):
    file_path = tmp_path / file_name
    await write_file(dict_value, file_path)
    assert file_path.exists()


@pytest.mark.asyncio
async def test_read_file(dict_value, file_name, tmp_path):
    await write_file(dict_value, tmp_path / file_name)
    data = await read_file(tmp_path / file_name)
    assert data == dict_value
