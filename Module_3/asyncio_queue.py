import asyncio


async def producer(queue, data):
    for value in data:
        await queue.put(value)
    await queue.put(None)


async def consumer(queue, queue_out):
    result = []
    while True:
        item = await queue.get()
        if item is None:
            break
        result.append(item)
    await queue_out.put(result)


async def main(data):
    queue = asyncio.Queue()
    queue_out = asyncio.Queue()
    await asyncio.gather(
        producer(queue, data),
        consumer(queue, queue_out)
    )
    return await queue_out.get()


if __name__ == "__main__":
    print(asyncio.run(main([i for i in range(5)])))
