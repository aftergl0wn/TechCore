import time

import pytest
from http import HTTPStatus


@pytest.mark.asyncio
async def test_get(
    app, async_client, review_response,
    book_response, delay_book, delay_review, mocker
):
    mocker.patch(
        'app.service.ReviewRepository.get_product_id',
        new=mocker.AsyncMock(side_effect=[delay_review])
    )
    mocker.patch(
        'app.crud.crud_book.BookRepository.get_by_id',
        new=mocker.AsyncMock(side_effect=[delay_book])
    )
    start = time.time()
    response = await async_client.get(
        "/api/products/1/details"
    )
    assert time.time() - start < 2
    assert response.status_code == HTTPStatus.OK
    assert response.json()["book"]["id"] == book_response.id
    assert response.json()["reviews"][0]["product_id"] == review_response.product_id
