import asyncio

from fastapi import FastAPI

from app.deps_redis import background_service_cache
from app.routers.book import router


app = FastAPI()
app.include_router(router)

background_task = None


@app.on_event("startup")
async def startup():
    global background_task
    background_task = asyncio.create_task(background_service_cache())


@app.on_event("shutdown")
async def shutdown():
    if background_task:
        background_task.cancel()
