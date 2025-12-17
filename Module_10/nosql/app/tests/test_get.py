import time

from http import HTTPStatus
from fastapi.testclient import TestClient

from app.crud.crud import AnalyticsRepository
from main import app


def test_get_book():
    client = TestClient(app)
    response = client.get("/books/1")
    time.sleep(2)
    collection = AnalyticsRepository.get_collection()
    last_doc = collection.find_one(
        {"book_id": 1},
        sort=[("_id", -1)]
    )
    assert response.status_code == HTTPStatus.OK
    assert last_doc["book_id"] == 1
