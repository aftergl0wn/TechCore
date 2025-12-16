import pytest
import pytest_asyncio
from aiohttp import web
from aiohttp.test_utils import TestServer


@pytest.fixture
def handler():
    async def handler_func(request):
        return web.json_response({"name": "Tom"})
    return handler_func


@pytest_asyncio.fixture
async def test_server(handler):
    app = web.Application()
    app.router.add_get("/test", handler)
    server = TestServer(app)
    await server.start_server()
    yield server
    await server.close()
