import os

import pytest

from .js import read_file, write_file


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


def test_write_file(dict_value, file_name):
    write_file(dict_value, file_name)
    assert os.path.exists(file_name)


def test_read_file(dict_value, file_name):
    write_file(dict_value, file_name)
    data = read_file(file_name)
    assert data == dict_value
