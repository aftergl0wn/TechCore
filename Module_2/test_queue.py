import multiprocessing
import pytest

from .multiprocessing_queue import consumer_multi, producer_multi


@pytest.fixture
def data():
    return [i for i in range(5)]


def test_queue(data, capsys):
    print('Начало работы основного потока')
    queue = multiprocessing.Queue()
    queue_out = multiprocessing.Queue()
    producer_multi(queue, data)
    consumer_multi(queue, queue_out)
    print('Окончание работы основного потока')
    captured = capsys.readouterr()
    assert queue_out.get(timeout=2) == data
    assert 'Начало работы основного потока' in captured.out
    assert 'Окончание работы основного потока' in captured.out
