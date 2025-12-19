import json

from confluent_kafka import Producer
from opentelemetry.propagate import inject


def send_book(producer: Producer, book_id: int):
    headers = {}
    inject(headers)
    kafka_headers = {
        k: v.encode() if isinstance(v, str) else v
        for k, v in headers.items()
    }

    message = json.dumps({"book_id": book_id}).encode("utf-8")
    producer.produce("book_views", value=message, headers=kafka_headers)
    producer.flush()
