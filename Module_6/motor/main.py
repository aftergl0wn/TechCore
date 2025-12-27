import motor.motor_asyncio
from fastapi import FastAPI

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")


@app.get("/ping-motor")
async def ping():
    return await client.admin.command("ping")
