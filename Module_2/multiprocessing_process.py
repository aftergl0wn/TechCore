import multiprocessing


def sum_process(value):
    value = sum(range(value))
    print(value)
    return value


def multi_process(process, *args):
    multi = multiprocessing.Process(target=process, args=args)
    multi.start()
    return multi


if __name__ == "__main__":
    print('Начало работы основного потока')
    multi_process(sum_process, 100_000_000)
    print('Окончание работы основного потока')
