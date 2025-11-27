import time

from .multiprocessing_process import multi_process, sum_process


def test_multiprocessing_process():
    flag_main = False
    start = time.time()
    multi_process(sum_process, 100_000_000)
    delta = time.time() - start
    assert delta < 1
    time.sleep(1)
    flag_main = True
    assert flag_main
