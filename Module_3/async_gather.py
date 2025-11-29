import asyncio


async def t(number):
    await asyncio.sleep(number)


async def main():
    result = await asyncio.gather(t(1), t(2), t(3))
    return result

if __name__ == "__main__":
    asyncio.run(main())
