import asyncio
import time

import httpx


async def main(number):
    URL = "http://jsonplaceholder.typicode.com/posts/1"
    timeout = httpx.Timeout(10)
    async with httpx.AsyncClient(timeout=timeout) as client:
        result = await asyncio.gather(
            *[client.get(URL) for _ in range(number)]
        )
        return result

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main(1))
    print(time.time()-start)
