import os

from celery import Celery
from dotenv import load_dotenv

from app.tracing import setup_zipkin_tracing

load_dotenv()

celery_app = Celery(
    "app",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_BACKEND_URL")
)

setup_zipkin_tracing("order-worker", celery_app=celery_app)
