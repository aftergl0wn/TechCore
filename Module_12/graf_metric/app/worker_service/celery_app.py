import os

from celery import Celery
from dotenv import load_dotenv
from prometheus_client import start_http_server

from app.tracing import setup_zipkin_tracing

load_dotenv()

celery_app = Celery(
    "app",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_BACKEND_URL")
)

setup_zipkin_tracing("order-worker", celery_app=celery_app)
start_http_server(int(os.getenv("METRICS_PORT_CELERY")))
