import pytest

from app.schemas import (
    ReviewRequestSchema,
    ReviewResponseSchema,
    ReviewUpdateSchema
)


@pytest.fixture
def mock_collection(mocker):
    return mocker.MagicMock()


@pytest.fixture
def review_request():
    return ReviewRequestSchema(
        product_id="pr1",
        rating=5,
        comment="Ok"
    )


@pytest.fixture
def review_response():
    return ReviewResponseSchema(
        id="st1",
        product_id="pr1",
        rating=5,
        comment="Ok"
    )


@pytest.fixture
def review_update():
    return ReviewUpdateSchema(
        rating=4,
    )


@pytest.fixture
def review_response_update():
    return ReviewResponseSchema(
        id="st1",
        product_id="pr1",
        rating=4,
        comment="Ok"
    )
