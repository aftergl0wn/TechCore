import os

from confluent_kafka import Producer
from dotenv import load_dotenv

load_dotenv()


def create_producer():
    config = {
        "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    }
    return Producer(config)
