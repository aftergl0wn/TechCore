import asyncio
import logging


async def wait():
    try:
        await asyncio.wait_for(
            asyncio.sleep(5),
            timeout=2
        )
    except TimeoutError:
        logging.error("Лимит времени исчерпан")


if __name__ == "__main__":
    asyncio.run(wait())
