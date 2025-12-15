from service import WorkerService


def test_celery_que(mock_sleep, caplog):
    mock, count = mock_sleep
    WorkerService.task_reject_on_worker_lost.delay(111)
    assert count[0] == 3
    assert "reject requeue=False" in caplog.text
