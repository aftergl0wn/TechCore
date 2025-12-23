import asyncio

import structlog
from fastapi import FastAPI
from fastapi.responses import Response

from app.kafka.analytics_worker import consume_messages
from app.routers.book import router
from app.routers.router_mongo import router_review
from app.tracing import get_prometheus_metrics, setup_zipkin_tracing

structlog.configure(processors=[structlog.processors.JSONRenderer()])
logger = structlog.get_logger(__name__)

app = FastAPI()
app.include_router(router, prefix="/api")
app.include_router(router_review, prefix="/api")
setup_zipkin_tracing("book-service", app)


@app.get("/healthz")
async def healthz_check():
    return {"status": "ok"}


@app.get("/metrics")
async def metrics_endpoint():
    metrics_data = get_prometheus_metrics()
    return Response(content=metrics_data, media_type="text/plain")


@app.on_event("startup")
async def startup_event():
    logger.info("startup", service="book-service")
    task = asyncio.create_task(consume_messages())
    app.state.consumer_task = task


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("shutdown", service="book-service")
    task = getattr(app.state, "consumer_task", None)
    if task is not None:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
