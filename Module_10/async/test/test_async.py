import pytest
from aiokafka import AIOKafkaConsumer

from app.kafka.analytics_worker import create_consumer


@pytest.mark.asycnio
async def test_consumer():
    consumer = await create_consumer()
    assert isinstance(consumer, AIOKafkaConsumer)
    await consumer.stop()
