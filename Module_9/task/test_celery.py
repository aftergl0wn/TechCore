from service import WorkerService


def test_celery():
    task = WorkerService.process_order.delay(1)
    assert task.get(timeout=15) == "Done 1"
