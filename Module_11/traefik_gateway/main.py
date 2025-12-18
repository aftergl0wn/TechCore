import asyncio

from fastapi import FastAPI

from app.kafka.analytics_worker import consume_messages
from app.routers.book import router
from app.routers.router_mongo import router_review

app = FastAPI()
app.include_router(router, prefix="/api")
app.include_router(router_review, prefix="/api")


@app.on_event("startup")
async def startup_event():
    task = asyncio.create_task(consume_messages())
    app.state.consumer_task = task


@app.on_event("shutdown")
async def shutdown_event():
    task = getattr(app.state, "consumer_task", None)
    if task is not None:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
