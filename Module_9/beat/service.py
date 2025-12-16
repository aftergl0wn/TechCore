from worker_service.celery_app import celery_app


class WorkerService:
    @staticmethod
    @celery_app.task
    def nightly_report():
        return "Night report"
