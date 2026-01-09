import httpx


class AuthorService:
    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url)
