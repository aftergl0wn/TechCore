from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

client = AsyncIOMotorClient()
db = client.reviews


def collection() -> AsyncIOMotorCollection:
    return client.db.reviews
