import json
import os

from confluent_kafka import Consumer
from dotenv import load_dotenv

from app.crud.crud import AnalyticsRepository

load_dotenv(".env")


def create_consumer():
    bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    config = {
        "bootstrap.servers": bootstrap,
        "group.id": "analytics",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": True,
    }
    return Consumer(config)


def consume_messages():
    consumer = create_consumer()
    consumer.subscribe(["book_views"])
    analytics_collection = AnalyticsRepository.get_collection()

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            continue
        payload = json.loads(msg.value().decode("utf-8"))
        AnalyticsRepository.save_message(payload, analytics_collection)


if __name__ == "__main__":
    consume_messages()
