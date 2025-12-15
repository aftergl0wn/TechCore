import aiohttp
import asyncio


class AuthorService:
    def __init__(self, base_url: str):
        self.async_session = aiohttp.ClientSession()
        self.base_url = base_url

    async def get(self, path: str):
        url = f"{self.base_url}{path}"
        try:
            async with self.async_session as session:
                return await asyncio.wait_for(session.get(url), timeout=2.0)
        except asyncio.TimeoutError:
            raise TimeoutError("Time out")
