import time


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f"Execution time: {time.time() - start_time:.1f}s")
        return result
    return wrapper


if __name__ == "__main__":

    @timer
    def time_sleep():
        time.sleep(1)
    time_sleep()

    # Вызов без синтаксического сахара
    timer(time.sleep)(1)
