import asyncio
import json
import os

from aiokafka import AIOKafkaConsumer
from dotenv import load_dotenv

from app.crud.crud import AnalyticsRepository

load_dotenv(".env")


async def create_consumer():
    bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    consumer = AIOKafkaConsumer(
        "book_views",
        bootstrap_servers=bootstrap,
        group_id="analytics",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )
    await consumer.start()
    return consumer


async def consume_messages():
    consumer = await create_consumer()
    analytics_collection = AnalyticsRepository.get_collection()

    try:
        async for msg in consumer:
            payload = json.loads(msg.value.decode("utf-8"))
            AnalyticsRepository.save_message(payload, analytics_collection)
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_messages())
