import multiprocessing


def sum_process(value):
    value = sum(range(value))
    return value


def multi_pool(process, value):
    with multiprocessing.Pool(4) as p:
        result = p.map(process, value)
    return result


if __name__ == "__main__":
    print('Начало работы основного потока')
    answer = multi_pool(sum_process, range(100_000_000, 100_000_010))
    print(answer)
    print('Окончание работы основного потока')
