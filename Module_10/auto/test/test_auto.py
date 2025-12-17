from app.kafka.analytics_worker import create_consumer


def test_consumer(mocker):
    captured = {}

    class TestConsumer:
        def __init__(self, config):
            captured["config"] = config

    mocker.patch("app.kafka.analytics_worker.Consumer", TestConsumer)

    create_consumer()
    assert captured["config"]["enable.auto.commit"] is False
