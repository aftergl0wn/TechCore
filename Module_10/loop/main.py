import threading

from fastapi import FastAPI

from app.kafka.analytics_worker import consume_messages
from app.routers.book import router


app = FastAPI()
app.include_router(router)


def _run_consumer():
    consume_messages()


@app.on_event("startup")
async def startup_event():
    t = threading.Thread(
        target=_run_consumer, name="kafka-consumer", daemon=True
    )
    t.start()


@app.on_event("shutdown")
async def shutdown_event():
    task = getattr(app.state, "consumer_task", None)
    if task is not None:
        task.cancel()
