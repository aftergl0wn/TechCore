from service import WorkerService


def test_celery_retry(mock_sleep):
    mock, count = mock_sleep
    task = WorkerService.process_order.delay(111)
    result = task.get()
    assert result == "Done 111"
    assert count[0] == 3
