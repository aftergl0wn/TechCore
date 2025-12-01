import asyncio
import aiofiles


async def stream_data(file):
    async with aiofiles.open(file, "r", encoding="utf-8") as f:
        async for value in f:
            yield value.strip()
            await asyncio.sleep(1)


async def main():
    async for value in stream_data("text.txt"):
        print(value)


if __name__ == "__main__":
    asyncio.run(main())
