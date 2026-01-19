import asyncio
import httpx


class AuthorService:
    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url)

    async def get_parallel(self, path1: str, path2: str):
        return await asyncio.gather(
            self.client.get(path1),
            self.client.get(path2)
        )
