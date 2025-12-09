import logging
from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_post(async_client, value, author_data, caplog):
    with caplog.at_level(logging.INFO):
        response = await async_client.post("/books", json=value)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == value["title"]
    assert response.json()["author_id"] == 1


@pytest.mark.asyncio
async def test_get(async_client, value, caplog):
    with caplog.at_level(logging.INFO):
        await async_client.post("/books", json=value)
        response = await async_client.get("/books/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == value["title"]
    assert response.json()["author_id"] == 1


@pytest.mark.asyncio
async def test_error_get(async_client, caplog):
    with caplog.at_level(logging.INFO):
        response = await async_client.get("/books/1")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found'}
