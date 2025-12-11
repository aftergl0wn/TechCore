from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()
motor_client = AsyncIOMotorClient()


@app.get("/ping-motor")
async def ping():
    return await motor_client.admin.command("ping")
