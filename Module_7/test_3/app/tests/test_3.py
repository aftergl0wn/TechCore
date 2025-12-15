import pytest

from app.crud import BookRepository
from app.service import BookService


@pytest.mark.asyncio
async def test_get_id(book, session, mocker):
    mocker.patch.object(
        BookRepository,
        "get_by_id",
        mocker.AsyncMock(return_value=book)
    )
    result = await BookService.get_by_id(1, session)
    assert result == book


@pytest.mark.asyncio
async def test_create(book, book_schema, session, mocker):
    mocker.patch.object(
        BookRepository,
        "create",
        mocker.AsyncMock(return_value=book)
    )
    result = await BookService.create(book_schema, session)
    assert result == book


@pytest.mark.asyncio
async def test_get_all(book, session, mocker):
    mocker.patch.object(
        BookRepository,
        "get_all",
        mocker.AsyncMock(return_value=[book,])
    )
    result = await BookService.get_all(session)
    assert result == [book,]


@pytest.mark.asyncio
async def test_update(book, book_old, book_schema, session, mocker):
    mocker.patch.object(
        BookRepository,
        "update",
        mocker.AsyncMock(return_value=book)
    )
    result = await BookService.update(book_old, book_schema, session)
    assert result == book


@pytest.mark.asyncio
async def test_delete(book, session, mocker):
    mocker.patch.object(
        BookRepository,
        "delete",
        mocker.AsyncMock(return_value=True)
    )
    result = await BookService.delete(book, session)
    assert result is True
