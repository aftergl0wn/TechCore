import logging

import pytest

from .exception_handling import (
    exception_handling_v1, exception_handling_v2,
    exception_handling_v3, exception_handling_v4
)


@pytest.fixture
def text():
    return "Harry, you're wizard"


@pytest.fixture
def file_name(tmp_path):
    return tmp_path / "Message"


@pytest.fixture
def write_file():
    def _write(name, value):
        with open(name, "w", encoding="utf-8") as f:
            f.write(value)
    return _write


@pytest.fixture
def error_open(monkeypatch):
    def _open(*args, **kwargs):
        raise PermissionError("Some Error")
    monkeypatch.setattr("builtins.open", _open)


def test_file_v1(write_file, text, file_name, capsys):
    write_file(file_name, text)
    result = exception_handling_v1(file_name)
    assert result == text
    captured = capsys.readouterr()
    assert "Done" in captured.out
    assert "Exit" not in captured.out


def test_error_file_v1(file_name, error_open, capsys, caplog):
    with caplog.at_level(logging.ERROR):
        result = exception_handling_v1(file_name)
    assert result is None
    captured = capsys.readouterr()
    assert "Done" in captured.out
    assert "Some Error" in caplog.text
    assert "Exit" in captured.out


def test_no_file_v1(file_name, capsys):
    result = exception_handling_v1(file_name)
    assert result is None
    captured = capsys.readouterr()
    assert "Done" in captured.out
    # Проверка, что "Exit" не выведется
    # При обработке ошибки функция возращает None
    assert "Exit" not in captured.out


def test_no_file_v2(file_name, capsys):
    result = exception_handling_v2(file_name)
    assert result is None
    captured = capsys.readouterr()
    assert "Done" in captured.out
    # Проверка, что "Exit" выведется
    # При обработке ошибки функция ничего не делает и продолжает работу дальше
    assert "Exit" in captured.out


def test_no_file_v3(file_name, capsys):
    result = exception_handling_v3(file_name)
    captured = capsys.readouterr()
    # Проверка что функция возвращает "Done"
    # При обработке ошибки функция ничего не делает и продолжает работу дальше
    assert result == "Done"
    # "Exit" не выведется никогда
    # так как в блоке finally есть return
    assert "Exit" not in captured.out


def test_no_file_v4(file_name, capsys):
    result = exception_handling_v4(file_name)
    captured = capsys.readouterr()
    # Проверка что функция возвращает "Done"
    # При обработке ошибки функция возращает None,
    # но finally выполняется в любом случае,
    # поэтому блок finally перезаписывает None на "Done"
    assert result == "Done"
    # "Exit" не выведется никогда
    # так как в блоке finally есть return
    assert "Exit" not in captured.out
