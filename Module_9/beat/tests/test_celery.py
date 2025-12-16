from worker_service.celery_app import celery_app


def test_beat_schedule():
    schedule = celery_app.conf.beat_schedule["nightly-report-task"]
    assert "nightly-report-task" in celery_app.conf.beat_schedule
    assert schedule["task"] == "service.WorkerService.nightly_report"
    assert schedule["schedule"] == 300
