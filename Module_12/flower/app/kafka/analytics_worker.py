import asyncio
import json
import os

import structlog
from aiokafka import AIOKafkaConsumer
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.propagate import extract
from prometheus_client import start_http_server

from app.crud.crud import AnalyticsRepository
from app.tracing import setup_zipkin_tracing

load_dotenv(".env")

structlog.configure(processors=[structlog.processors.JSONRenderer()])
logger = structlog.get_logger(__name__)

setup_zipkin_tracing("analytics-worker")
start_http_server(int(os.getenv("METRICS_PORT")))

tracer = trace.get_tracer(__name__)


async def create_consumer():
    bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    logger.info("create_kafka_consumer", bootstrap_servers=bootstrap)
    consumer = AIOKafkaConsumer(
        "book_views",
        bootstrap_servers=bootstrap,
        group_id="analytics",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )
    await consumer.start()
    logger.info("kafka_cinsumer_started")
    return consumer


async def consume_messages():
    logger.info("starting_analytics_worker")
    consumer = await create_consumer()
    analytics_collection = AnalyticsRepository.get_collection()

    try:
        async for msg in consumer:
            headers = {
                k: v.decode() if isinstance(v, bytes) else v
                for k, v in (msg.headers or {}).items()
            }
            context = extract(headers)

            with tracer.start_as_current_span(
                "kafka.receive", context=context
            ):
                payload = json.loads(msg.value.decode("utf-8"))
                logger.info("message_received", book_id=payload.get("book_id"))
                AnalyticsRepository.save_message(
                    payload, analytics_collection
                )
                logger.info("message_saved", book_id=payload.get("book_id"))
    except Exception as e:
        logger.error("error_consuming_messages", error=str(e))
        raise
    finally:
        logger.info("stopping_consumer")
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume_messages())
