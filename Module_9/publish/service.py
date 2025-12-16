import time

from celery_app import celery_app


class WorkerService:
    @staticmethod
    @celery_app.task
    def process_order(order_id):
        time.sleep(10)
        return f"Done {order_id}"
