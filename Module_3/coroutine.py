import asyncio


async def fetch_data():
    await asyncio.sleep(1)
    return "Done"


async def main():
    result = await fetch_data()
    return result


if __name__ == "__main__":
    print(asyncio.run(main()))
