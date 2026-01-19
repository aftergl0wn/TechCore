import multiprocessing
import time


def sum_process(value, queue):
    value = sum(range(value))
    queue.put(value)


def multi_process(process, value, queue):
    multi = multiprocessing.Process(target=process, args=(value, queue))
    multi.start()
    return multi


def main_process():
    print('Начало работы основного потока')
    result_main = 0
    queue = multiprocessing.Queue()
    multi = multi_process(sum_process, 100_000_000, queue)
    for _ in range(5):
        result_main += 1
        time.sleep(1)
    multi.join()
    print(f'Результат работы дочернего потока:{queue.get()}')
    print(f'Результат работы основного потока:{result_main}')
    print('Окончание работы основного потока')


if __name__ == "__main__":
    main_process()
