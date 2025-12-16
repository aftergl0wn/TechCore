import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.kafka.analytics_worker import consume_messages
from app.routers.book import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(asyncio.to_thread(consume_messages))
    yield
    task.cancel()

app = FastAPI(redoc_url=None)
app.include_router(router)
