from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_cor_post(async_client, author_book_data, caplog):
    response = await async_client.post("/author_book", json=author_book_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["author"]["name"] == author_book_data["author"]["name"]
    assert response.json()["book"]["title"] == author_book_data["book"]["title"]


@pytest.mark.asyncio
async def test_err_post(async_client, setup_db_engine, value, caplog):
    response = await async_client.post("/author_book", json=value)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
