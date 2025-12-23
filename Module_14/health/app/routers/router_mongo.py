from fastapi import APIRouter, Depends
from http import HTTPStatus
from motor.motor_asyncio import AsyncIOMotorCollection

import structlog

from app.database import collection
from app.schema.schemas_mongo import (
    ReviewRequestSchema,
    ReviewResponseSchema,
    ReviewUpdateSchema
)
from app.service import ReviewService

logger = structlog.get_logger(__name__)
router_review = APIRouter()


@router_review.post(
    "/api/reviews",
    response_model=ReviewResponseSchema,
    status_code=HTTPStatus.CREATED,
)
async def create_new(
    review: ReviewRequestSchema,
    collection: AsyncIOMotorCollection = Depends(collection),
):
    logger.info("create_review_start", product_id=review.product_id)
    result = await ReviewService.create(review, collection)
    logger.info(
        "review_created",
        review_id=result.id,
        product_id=review.product_id
    )
    return result


@router_review.get(
    "/api/products/{id}/reviews",
    response_model=list[ReviewResponseSchema]
)
async def get_product(
    id: str,
    collection: AsyncIOMotorCollection = Depends(collection),
):
    logger.info("get_product_reviews_start", product_id=id)
    result = await ReviewService.get_product_id(id, collection)
    logger.info(
        "product_reviews_retrieved",
        product_id=id,
        count=len(result)
    )
    return result


@router_review.patch(
    "/api/reviews/{review_id}",
    response_model=ReviewResponseSchema
)
async def update_review(
    review_id: str,
    review: ReviewUpdateSchema,
    collection: AsyncIOMotorCollection = Depends(collection),
):
    logger.info("update_review_start", review_id=review_id)
    result = await ReviewService.update(review_id, review, collection)
    logger.info("review_updated", review_id=review_id)
    return result


@router_review.delete(
    "/api/reviews/{review_id}",
    status_code=HTTPStatus.NO_CONTENT
)
async def deler_review(
    review_id: str,
    collection: AsyncIOMotorCollection = Depends(collection),
):
    logger.info("delete_review_start", review_id=review_id)
    result = await ReviewService.delete(review_id, collection)
    logger.info("review_deleted", review_id=review_id, deleted=result)
    return result
