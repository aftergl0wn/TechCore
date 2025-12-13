import asyncio

import pytest
from http import HTTPStatus

from app.crud.crud import BookRepository
from app.model import Book


@pytest.mark.asyncio
async def test_lock(
    redis_mock_publish, db_session_mock, book_data_new, async_client, mocker
):
    lock_mock = mocker.AsyncMock()
    lock_mock.__aenter__ = mocker.AsyncMock(return_value=lock_mock)
    lock_mock.__aexit__ = mocker.AsyncMock(return_value=None)
    redis_mock_publish.lock = mocker.MagicMock(return_value=lock_mock)
    book = Book(id=1, title="Old")
    await BookRepository.update_book(book, 1, book_data_new, db_session_mock, redis_mock_publish)
    redis_mock_publish.lock.assert_called_once_with('inventory_lock:1', timeout=10)
