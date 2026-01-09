from http import HTTPStatus
from fastapi.testclient import TestClient

from main import app
from worker_service.celery_app import celery_app


def test_celery_worker_processes_task():
    celery_app.conf.task_always_eager = True
    client = TestClient(app)
    response = client.post("/order?order_id=123")
    assert response.status_code == HTTPStatus.ACCEPTED
    assert response.json() == {"message": "Done 123"}
