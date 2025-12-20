import os

import structlog
from celery import Celery
from dotenv import load_dotenv
from prometheus_client import start_http_server

from app.tracing import setup_zipkin_tracing

load_dotenv(".env")

structlog.configure(processors=[structlog.processors.JSONRenderer()])
logger = structlog.get_logger(__name__)

celery_app = Celery(
    "app",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_BACKEND_URL")
)

logger.info("initializing_celery_app", broker=os.getenv("CELERY_BROKER_URL"),)
setup_zipkin_tracing("order-worker", celery_app=celery_app)
start_http_server(int(os.getenv("METRICS_PORT_CELERY")))
logger.info(
    "order_worker_started",
    metrics_port=os.getenv("METRICS_PORT_CELERY")
)
