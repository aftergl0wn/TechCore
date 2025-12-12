import pytest

from app.service import ReviewRepository


@pytest.mark.asyncio
async def test_get(
    mock_collection, review_response, mocker
):
    answer = [review_response]
    mock_get = mocker.patch(
        'app.service.ReviewRepository.get_product_id',
        new=mocker.AsyncMock(side_effect=[answer])
    )
    result = await ReviewRepository.get_product_id(
        review_response.product_id,
        mock_collection
    )
    mock_get.assert_called_once_with(
        review_response.product_id,
        mock_collection
    )
    assert result == answer


@pytest.mark.asyncio
async def test_create(
    mock_collection, review_request, review_response, mocker
):
    mock_create = mocker.patch(
        'app.service.ReviewRepository.create',
        new=mocker.AsyncMock(side_effect=[review_response])
    )
    result = await ReviewRepository.create(
        review_request, mock_collection
    )
    mock_create.assert_called_once_with(
        review_request, mock_collection
    )
    assert result == review_response


@pytest.mark.asyncio
async def test_delete(
    mock_collection, review_request, review_response, mocker
):
    mock_delete = mocker.patch(
        'app.service.ReviewRepository.delete',
        new=mocker.AsyncMock(side_effect=[True])
    )
    result = await ReviewRepository.delete(
        review_response.id, mock_collection
    )
    mock_delete.assert_called_once_with(
        review_response.id, mock_collection
    )
    assert result is True


@pytest.mark.asyncio
async def test_update(
    mock_collection, review_update, review_response_update, mocker
):
    mock_update = mocker.patch(
        'app.service.ReviewRepository.update',
        new=mocker.AsyncMock(return_value=review_response_update)
    )
    result = await ReviewRepository.update(
        review_response_update.id, review_update, mock_collection
    )
    mock_update.assert_called_once_with(
        review_response_update.id, review_update, mock_collection
    )
    assert result == review_response_update
