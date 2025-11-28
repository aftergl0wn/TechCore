import multiprocessing


def producer(queue, value_list):
    for value in value_list:
        queue.put(value)
    queue.put(None)


def consumer(queue, queue_out):
    result = []
    while True:
        item = queue.get()
        if item is None:
            break
        result.append(item)
    queue_out.put(result)


def producer_multi(queue, data):
    producer_m = multiprocessing.Process(target=producer, args=(queue, data))
    producer_m.start()
    producer_m.join()


def consumer_multi(queue, queue_out):
    consumer_m = multiprocessing.Process(
        target=consumer, args=(queue, queue_out)
    )
    consumer_m.start()
    consumer_m.join()


if __name__ == "__main__":
    print('Начало работы основного потока')
    data = [i for i in range(5)]
    queue = multiprocessing.Queue()
    queue_out = multiprocessing.Queue()
    producer_multi(queue, data)
    consumer_multi(queue, queue_out)
    print(queue_out.get(timeout=2))
    print('Окончание работы основного потока')
