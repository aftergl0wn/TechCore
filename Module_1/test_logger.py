import pytest

from .logger import logger


def test_logger_one_value(capsys):
    logger("Hello")
    captured = capsys.readouterr()
    assert "1. Hello" in captured.out


def test_logger_more_value(capsys):
    logger("Hello", 30, name="Harry")
    captured = capsys.readouterr()
    assert "1. Hello" in captured.out
    assert "2. 30" in captured.out
    assert "name: Harry" in captured.out


def test_logger_no_value():
    with pytest.raises(TypeError):
        logger()
