import asyncio

import backoff
import httpx


class AuthorService:
    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url)

    @backoff.on_exception(backoff.expo, httpx.HTTPStatusError, max_tries=3)
    async def get(self, path: str):
        try:
            response = await asyncio.wait_for(self.client.get(path), timeout=2.0)
            response.raise_for_status()
            return response
        except asyncio.TimeoutError:
            raise TimeoutError("Time out")
