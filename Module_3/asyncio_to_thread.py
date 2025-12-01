import asyncio
import time


def old_func():
    time.sleep(5)
    return "End work old_func"


async def data(result):
    for i in range(5):
        result.append(i)
        await asyncio.sleep(1)
    return result


async def main():
    task = await asyncio.gather(
        asyncio.to_thread(old_func),
        data([])
    )
    return task


if __name__ == "__main__":
    start = time.time()
    print(asyncio.run(main()))
    print(time.time() - start)
