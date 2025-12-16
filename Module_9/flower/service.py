from worker_service.celery_app import celery_app


class WorkerService:
    @staticmethod
    @celery_app.task(name="service.WorkerService.nightly_report")
    def nightly_report():
        return "Night report"
