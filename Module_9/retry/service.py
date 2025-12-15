import time

from worker_service.celery_app import celery_app


class WorkerService:
    @staticmethod
    @celery_app.task(bind=True)
    def process_order(self, order_id):
        try:
            time.sleep(10)
            return f"Done {order_id}"
        except Exception as exc:
            raise self.retry(exc=exc, countdown=5,  max_retries=3)
