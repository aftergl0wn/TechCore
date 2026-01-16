import asyncio


async def get_info(lock):
    async with lock:
        await asyncio.sleep(1)
    return "data"


async def main():
    lock = asyncio.Lock()
    result = await asyncio.gather(
        *[get_info(lock) for _ in range(10)]
    )
    return result


if __name__ == "__main__":
    asyncio.run(main())
