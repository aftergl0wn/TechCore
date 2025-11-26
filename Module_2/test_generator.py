import types
import json

import pytest

from .generator import read_large_log


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


@pytest.fixture
def file_json(tmp_path):
    def _write(data):
        file_name = tmp_path / "test"
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return file_name
    return _write


@pytest.fixture
def file_text(tmp_path):
    def _write(data):
        file_name = tmp_path / "test"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(data)
        return file_name
    return _write


def test_attr_gen(data, file_json):
    file = file_json(data)
    gen = read_large_log(file)
    assert isinstance(gen, types.GeneratorType)
    assert hasattr(gen, "__iter__")
    assert hasattr(gen, "__next__")


def test_value_gen(data, file_json):
    file = file_json(data)
    gen = read_large_log(file)
    list_gen = [i for i in gen if i != "{" and i != "}"]
    assert len(data) == len(list_gen)
    assert f'"name": "{data["name"]}",' == list_gen[0]
    assert f'"age": {data["age"]},' == list_gen[1]
    assert f'"home": "{data["home"]}"' == list_gen[2]


def test_iter_gen(data, file_json):
    file = file_json(data)
    gen = read_large_log(file)
    list(gen)
    with pytest.raises(StopIteration):
        next(gen)


def test_str_gen(data_str, file_text):
    file = file_text(data_str)
    gen = read_large_log(file)
    assert next(gen) == "a"
    assert next(gen) == "b"
    assert next(gen) == "c"


def test_len_str_gen(data_str, file_text):
    file = file_text(data_str)
    gen = read_large_log(file)
    list_one = list(gen)
    list_two = list(gen)
    assert len(list_one) == 3
    assert len(list_two) == 0
