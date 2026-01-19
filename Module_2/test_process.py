import time

from .multiprocessing_process import main_process


def test_multiprocessing_process(capsys):
    start = time.time()
    main_process()
    captured = capsys.readouterr()
    assert time.time() - start < 6
    assert 'Начало работы основного потока' in captured.out
    assert 'Результат работы дочернего потока:4999999950000000' in captured.out
    assert 'Результат работы основного потока:5' in captured.out
    assert 'Окончание работы основного потока' in captured.out
