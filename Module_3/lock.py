import asyncio
import logging

import httpx


async def response_url():
    URL = "http://jsonplaceholder.typicode.com/posts/1"
    async with httpx.AsyncClient() as client:
        response = await client.get(URL)
    return response


async def get_info(coroutine, key, lock, cache, queue):
    async with lock:
        await queue.put(coroutine)
        if key not in cache:
            cache[key] = await response_url()
        if queue.qsize() > 1:
            logging.error("Обнаружено больше одной корутины")
        await queue.get()
    return cache[key]


async def main():
    cache = dict()
    lock = asyncio.Lock()
    queue = asyncio.Queue()
    result = await asyncio.gather(
        *[get_info(i, "cache", lock, cache, queue) for i in range(10)]
    )
    return result


if __name__ == "__main__":
    asyncio.run(main())
