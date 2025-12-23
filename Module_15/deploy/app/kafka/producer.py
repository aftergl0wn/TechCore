import os

from confluent_kafka import Producer
from dotenv import load_dotenv

load_dotenv(".env")


def create_producer():
    config = {
        "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    }
    return Producer(config)
