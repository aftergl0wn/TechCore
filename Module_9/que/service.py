import time

from celery.exceptions import Reject

from worker_service.celery_app import celery_app


class WorkerService:
    @staticmethod
    @celery_app.task(bind=True, max_retries=3)
    def task_reject_on_worker_lost(self, order_id):
        try:
            time.sleep(10)
            return f"Done {order_id}"
        except Exception as exc:
            if self.request.retries >= self.max_retries - 1:
                raise Reject(exc, requeue=False)
            raise self.retry(exc=exc)
