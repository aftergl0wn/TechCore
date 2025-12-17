import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()


celery_app = Celery(
    "app",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_BACKEND_URL")
)

celery_app.conf.update(
    beat_schedule={
        "nightly-report-task": {
            "task": "service.WorkerService.nightly_report",
            "schedule": 30,
        }
    },
    worker_send_task_events=True,
    task_send_sent_event=True,
)

