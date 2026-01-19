import pytest
from http import HTTPStatus


@pytest.mark.asyncio
async def test_get(
    app, async_client, review_response, mocker
):
    answer = [review_response]
    mocker.patch(
        'app.service.ReviewRepository.get_product_id',
        new=mocker.AsyncMock(side_effect=[answer])
    )
    response = await async_client.get(
        f"/api/products/{review_response.id}/reviews"
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()[0]["_id"] == review_response.id
    assert response.json()[0]["rating"] == review_response.rating


@pytest.mark.asyncio
async def test_create(
    app, async_client, review_request, review_response, mocker
):
    mocker.patch(
        'app.service.ReviewRepository.create',
        new=mocker.AsyncMock(side_effect=[review_response])
    )
    response = await async_client.post(
        "/api/reviews",
        json=review_request.dict()
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["_id"] == review_response.id
    assert response.json()["rating"] == review_response.rating


@pytest.mark.asyncio
async def test_delete(
    app, async_client, review_response, mocker
):
    mocker.patch(
        'app.service.ReviewRepository.delete',
        new=mocker.AsyncMock(side_effect=[True])
    )
    response = await async_client.delete(
        f"/api/reviews/{review_response.id}"
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.json() is True


@pytest.mark.asyncio
async def test_update(
    app, async_client, review_update, review_response_update, mocker
):
    mocker.patch(
        'app.service.ReviewRepository.update',
        new=mocker.AsyncMock(side_effect=[review_response_update])
    )
    response = await async_client.patch(
        f"/api/reviews/{review_response_update.id}",
        json=review_update.dict()
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["_id"] == review_response_update.id
    assert response.json()["rating"] == review_response_update.rating
