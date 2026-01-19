import types
import json

import aiofiles
import pytest
import pytest_asyncio

from .async_generator import stream_data


@pytest.fixture
def data():
    return {
        "name": "Tom",
        "age": 22,
        "home": "Vl"
    }


@pytest.fixture
def data_str():
    return "   a    \n    b   \n   c  \n"


@pytest_asyncio.fixture
async def file_json(tmp_path):
    async def _write(data):
        file_name = tmp_path / "test"
        data_json = json.dumps(data, indent=4)
        async with aiofiles.open(file_name, "w", encoding="utf-8") as f:
            await f.write(data_json)
        return file_name
    return _write


@pytest_asyncio.fixture
async def file_text(tmp_path):
    async def _write(data):
        file_name = tmp_path / "test"
        async with aiofiles.open(file_name, "w", encoding="utf-8") as f:
            await f.write(data)
        return file_name
    return _write


@pytest.mark.asyncio
async def test_attr_gen(data, file_json):
    file = await file_json(data)
    gen = stream_data(file)
    assert isinstance(gen, types.AsyncGeneratorType)
    assert hasattr(gen, "__aiter__")
    assert hasattr(gen, "__anext__")


@pytest.mark.asyncio
async def test_value_gen(data, file_json):
    file = await file_json(data)
    gen = stream_data(file)
    list_gen = [i async for i in gen if i != "{" and i != "}"]
    assert len(data) == len(list_gen)
    assert f'"name": "{data["name"]}",' == list_gen[0]
    assert f'"age": {data["age"]},' == list_gen[1]
    assert f'"home": "{data["home"]}"' == list_gen[2]


@pytest.mark.asyncio
async def test_iter_gen(data, file_json):
    file = await file_json(data)
    gen = stream_data(file)
    [i async for i in gen]
    with pytest.raises(StopAsyncIteration):
        await anext(gen)


@pytest.mark.asyncio
async def test_str_gen(data_str, file_text):
    file = await file_text(data_str)
    gen = stream_data(file)
    assert await anext(gen) == "a"
    assert await anext(gen) == "b"
    assert await anext(gen) == "c"


@pytest.mark.asyncio
async def test_len_str_gen(data_str, file_text):
    file = await file_text(data_str)
    gen = stream_data(file)
    list_one = [i async for i in gen]
    list_two = [i async for i in gen]
    assert len(list_one) == 3
    assert len(list_two) == 0
