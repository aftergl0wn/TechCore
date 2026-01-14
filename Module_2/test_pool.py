import pytest
import time

from .multiprocessing_pool import main_process


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


def test_pool_sync(value, result, capsys):
    main_process(False, value)
    captured = capsys.readouterr()
    assert 'Начало работы основного потока' in captured.out
    assert 'Результат работы дочернего потока:' in captured.out
    assert str(result) in captured.out
    assert 'Результат работы основного потока:5' in captured.out
    assert 'Окончание работы основного потока' in captured.out


def test_pool_async(value, result, capsys):
    main_process(True, value)
    captured = capsys.readouterr()
    assert 'Начало работы основного потока' in captured.out
    assert 'Результат работы дочернего потока:' in captured.out
    assert str(result) in captured.out
    assert 'Результат работы основного потока:5' in captured.out
    assert 'Окончание работы основного потока' in captured.out


def test_pool_diff(value):
    start_sync = time.time()
    # map блокирует основной поток
    # Здачи из основго потока будут выполнены только после map
    main_process(False, value)
    diff_sync = time.time() - start_sync
    start_async = time.time()
    # apply_async не блокирует основной поток
    # Здачи из основго потока будут выполнены параллельно с apply_async
    main_process(True, value)
    diff_async = time.time() - start_async
    assert diff_sync > diff_async
    assert diff_sync - diff_async > 4
