from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.schema.schemas_mongo import (
    ReviewRequestSchema,
    ReviewResponseSchema,
    ReviewUpdateSchema
)


class ReviewRepository:

    @staticmethod
    async def create(
        review: ReviewRequestSchema,
        collection: AsyncIOMotorCollection,
    ) -> ReviewResponseSchema:
        new_review_data = review.dict()
        result = await collection.insert_one(new_review_data)
        new_review = await collection.find_one(
            {"_id": result.inserted_id}
        )
        new_review["_id"] = str(new_review["_id"])
        return ReviewResponseSchema(**new_review)

    @staticmethod
    async def get_product_id(
        product_id: str,
        collection: AsyncIOMotorCollection
    ) -> list[ReviewResponseSchema]:
        cursor = collection.find(
            {"product_id": product_id}
        )
        data = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            data.append(ReviewResponseSchema(**doc))
        return data

    @staticmethod
    async def delete(
        review_id: str,
        collection: AsyncIOMotorCollection,
    ) -> bool:
        result = await collection.delete_one(
            {"_id": ObjectId(review_id)}
        )
        return result.deleted_count == 1

    @staticmethod
    async def update(
        review_id: str,
        review: ReviewUpdateSchema,
        collection: AsyncIOMotorCollection,
    ) -> ReviewResponseSchema:
        update_data = review.dict(exclude_unset=True)
        await collection.update_one(
            {"_id": ObjectId(review_id)},
            {"$set": update_data}
        )
        data_new = await collection.find_one(
            {"_id": ObjectId(review_id)}
        )
        data_new["_id"] = str(data_new["_id"])
        return ReviewResponseSchema(**data_new)
