import redis.asyncio as redis


def redis_client():
    return redis.Redis(decode_responses=True)
