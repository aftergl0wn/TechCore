from http import HTTPStatus
from fastapi.testclient import TestClient

from app.crud import BookRepository
from app.main import app


def test_get_all(book, session, mocker):
    mocker.patch.object(
        BookRepository,
        "get_all",
        mocker.AsyncMock(return_value=[book,])
    )
    client = TestClient(app)
    response = client.get("/api/books")
    assert response.status_code == HTTPStatus.OK
