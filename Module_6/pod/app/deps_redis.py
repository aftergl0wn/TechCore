import redis.asyncio as redis


def redis_client():
    return redis.Redis(decode_responses=True)


async def background_service_cache():
    client = redis_client()
    pubsub = client.pubsub()
    await pubsub.subscribe("cache:invalidate")
    async for message in pubsub.listen():
        if message["type"] != "message":
            continue
        book_id = message["data"]
        await client.delete(f"book:{book_id}")
