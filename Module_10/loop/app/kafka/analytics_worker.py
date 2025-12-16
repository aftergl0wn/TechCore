import os

from confluent_kafka import Consumer
from dotenv import load_dotenv

load_dotenv()


def create_consumer():
    config = {
        "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        "group.id": "analytics"
    }
    return Consumer(config)


def consume_messages():
    consumer = create_consumer()
    consumer.subscribe(["book_views"])
    while True:
        msg = consumer.poll(1.0)
