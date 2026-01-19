import asyncio

import httpx


class AuthorService:
    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url)

    async def get(self, path: str):
        try:
            return await asyncio.wait_for(self.client.get(path), timeout=2.0)
        except asyncio.TimeoutError:
            raise TimeoutError("Time out")
