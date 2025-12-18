import json

from confluent_kafka import Producer


def send_book(producer: Producer, book_id: int):
    message = json.dumps({"book_id": book_id}).encode("utf-8")
    producer.produce("book_views", value=message)
    producer.flush()
