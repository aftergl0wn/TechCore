from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_post(async_client, value, value2, author_data):
    await async_client.post("/books", json=value)
    await async_client.post("/books", json=value2)
    response =  await async_client.get("/books_report")
    assert response.status_code == HTTPStatus.OK
    assert response.json()[0]["author_name"] == author_data["name"]
    assert response.json()[0]["earliest_year"] == value["year"]
    assert response.json()[0]["lastest_year"] == value2["year"]
