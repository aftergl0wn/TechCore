import pytest

from worker_service.celery_app import celery_app


@pytest.fixture
def mock_sleep(mocker):
    celery_app.conf.task_always_eager = True

    call_count = [0]

    def mock_sleep(*args):
        nonlocal call_count
        call_count[0] += 1
        if call_count[0] < 3:
            raise ConnectionError()

    with mocker.patch("service.time.sleep", side_effect=mock_sleep) as mock:
        yield mock, call_count
