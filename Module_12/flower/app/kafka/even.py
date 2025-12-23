import json

import structlog
from confluent_kafka import Producer
from opentelemetry.propagate import inject

logger = structlog.get_logger(__name__)


def send_book(producer: Producer, book_id: int):
    logger.info("send_book_start", book_id=book_id)
    headers = {}
    inject(headers)
    kafka_headers = {
        k: v.encode() if isinstance(v, str) else v
        for k, v in headers.items()
    }

    message = json.dumps({"book_id": book_id}).encode("utf-8")
    producer.produce("book_views", value=message, headers=kafka_headers)
    producer.flush()
    logger.info("send_book_end", book_id=book_id)
