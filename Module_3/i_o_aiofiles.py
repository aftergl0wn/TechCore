import json

import aiofiles
import asyncio


async def write_file(dict_value, file):
    value = json.dumps(dict_value, indent=4, ensure_ascii=False)
    async with aiofiles.open(file, "w", encoding="utf-8") as f:
        await f.write(value)


async def read_file(file):
    async with aiofiles.open(file, "r", encoding="utf-8") as f:
        data = await f.read()
    return json.loads(data)


async def main():
    dict_value = {
        "name": "Алиса",
        "year": 2020,
        "message": "Hi",
    }
    await write_file(dict_value, "config.json")
    return await read_file("config.json")


if __name__ == "__main__":
    result = asyncio.run(main())
    print(result)
