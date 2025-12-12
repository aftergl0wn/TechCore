from fastapi import APIRouter, Depends
from http import HTTPStatus
from motor.motor_asyncio import AsyncIOMotorCollection

from .database import collection
from .schemas import (
    ReviewRequestSchema,
    ReviewResponseSchema,
    ReviewUpdateSchema
)
from .service import ReviewService


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
    return await ReviewService.create(review, collection)


@router_review.get(
    "/api/products/{id}/reviews",
    response_model=list[ReviewResponseSchema]
)
async def get_product(
    id: str,
    collection: AsyncIOMotorCollection = Depends(collection),
):
    return await ReviewService.get_product_id(id, collection)


@router_review.patch(
    "/api/reviews/{review_id}",
    response_model=ReviewResponseSchema
)
async def update_review(
    review_id: str,
    review: ReviewUpdateSchema,
    collection: AsyncIOMotorCollection = Depends(collection),
):
    return await ReviewService.update(review_id, review, collection)


@router_review.delete(
    "/api/reviews/{review_id}",
    status_code=HTTPStatus.NO_CONTENT
)
async def deler_review(
    review_id: str,
    collection: AsyncIOMotorCollection = Depends(collection),
):
    return await ReviewService.delete(review_id, collection)
