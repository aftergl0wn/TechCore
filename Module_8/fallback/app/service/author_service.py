from http import HTTPStatus

import httpx
from aiobreaker import CircuitBreaker, CircuitBreakerError


class AuthorService:
    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url)
        self.circuit_breaker = CircuitBreaker(fail_max=5)

    async def get(self, path: str):
        async def _get():
            response = await self.client.get(path)
            response.raise_for_status()
            return response
        try:
            return await self.circuit_breaker.call_async(_get)
        except CircuitBreakerError:
            return httpx.Response(
                status_code=HTTPStatus.OK,
                json={"name": "Default Author"}
            )
