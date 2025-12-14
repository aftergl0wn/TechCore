import asyncio
import httpx


class AuthorService:
    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url)
        self.semaphore = asyncio.Semaphore(5)

    async def get(self, path: str):
        async with self.semaphore:
            return await self.client.get(path)
