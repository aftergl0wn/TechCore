from aiobreaker import CircuitBreaker

import httpx


class AuthorService:
    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url)
        self.circuit_breaker = CircuitBreaker(fail_max=5)

    async def get(self, path: str):
        async def _get():
            response = await self.client.get(path)
            response.raise_for_status()
            return response
        return await self.circuit_breaker.call_async(_get)
