from motor.motor_asyncio import AsyncIOMotorCollection

from app.crud.crud_review import ReviewRepository
from app.schema.schema_review import (
    ReviewRequestSchema,
    ReviewResponseSchema,
    ReviewUpdateSchema
)


class ReviewService:
    @staticmethod
    async def create(
        review: ReviewRequestSchema,
        collection: AsyncIOMotorCollection
    ) -> ReviewResponseSchema:
        return await ReviewRepository.create(review, collection)

    @staticmethod
    async def get_product_id(
        product_id: str,
        collection: AsyncIOMotorCollection
    ) -> list[ReviewResponseSchema]:
        return await ReviewRepository.get_product_id(product_id, collection)

    @staticmethod
    async def delete(
        review_id: str,
        collection: AsyncIOMotorCollection,
    ) -> bool:
        return await ReviewRepository.delete(review_id, collection)

    @staticmethod
    async def update(
        review_id: str,
        review: ReviewUpdateSchema,
        collection: AsyncIOMotorCollection,
    ) -> ReviewResponseSchema:
        return await ReviewRepository.update(review_id, review, collection)
