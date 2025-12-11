from fastapi import FastAPI
import redis.asyncio as redis

app = FastAPI()
redis_client = redis.Redis()


@app.get("/ping-redis")
async def ping():
    return await redis_client.ping()
