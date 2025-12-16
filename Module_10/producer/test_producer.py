from confluent_kafka import Producer

from producer import create_producer


def test_producer(mocker):
    producer = create_producer()
    assert isinstance(producer, Producer)
