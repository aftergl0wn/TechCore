import multiprocessing
import time


def sum_process(value):
    value = sum(range(value))
    return value


def multi_pool_map(process, value):
    with multiprocessing.Pool(4) as p:
        result = p.map(process, value)
    return result


def multi_pool_apply_async(process, value):
    pool = multiprocessing.Pool(4)
    return [
        pool.apply_async(process, args=(v,)) for v in value
    ]


def main_process(async_mode, value):
    print('Начало работы основного потока')
    result_main = 0
    if async_mode:
        multi = multi_pool_apply_async(sum_process, value)
    else:
        multi = multi_pool_map(sum_process, value)
    for _ in range(5):
        result_main += 1
        time.sleep(1)
    if async_mode:
        multi = [m.get() for m in multi]
    print(f'Результат работы дочернего потока:{multi}')
    print(f'Результат работы основного потока:{result_main}')
    print('Окончание работы основного потока')


if __name__ == "__main__":
    print('________________________________')
    main_process(False, range(100_000_000, 100_000_010))
    print('________________________________')
    main_process(True, range(100_000_000, 100_000_010))
    print('________________________________')
