import pytest

from .multiprocessing_pool import multi_pool, sum_process


@pytest.fixture
def result():
    return [
        4999999950000000, 5000000050000000,
        5000000150000001, 5000000250000003,
        5000000350000006, 5000000450000010,
        5000000550000015, 5000000650000021,
        5000000750000028, 5000000850000036
    ]


@pytest.fixture
def value():
    return range(100_000_000, 100_000_010)


def test_pool(value, result, capsys):
    print('Начало работы основного потока')
    answer = multi_pool(sum_process, value)
    print('Окончание работы основного потока')
    captured = capsys.readouterr()
    assert answer == result
    assert 'Начало работы основного потока' in captured.out
    assert 'Окончание работы основного потока' in captured.out
