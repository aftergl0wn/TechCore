import os

from celery import Celery
from dotenv import load_dotenv
from kombu import Queue

load_dotenv()


celery_app = Celery(
    "app",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_BACKEND_URL")
)

celery_app.conf.update(
    task_reject_on_worker_lost=True,
    task_acks_late=True,
    task_default_max_retries=3,
    task_queues=(
        Queue("celery", queue_arguments={
            "x-dead-letter-exchange": "celery",
            "x-dead-letter-routing-key": "celery._dlq",
        }),
        Queue("celery._dlq"),
    ),
)
