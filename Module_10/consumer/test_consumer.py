from confluent_kafka import Consumer

from analytics_worker import create_consumer


def test_consumer(mocker):
    consumer = create_consumer()
    assert isinstance(consumer, Consumer)
