import pytest


@pytest.mark.parametrize(
    "container_name",
    [
        "db", "redis", "rabbitmq", "zipkin",
        "zookeeper", "mongo", "kafka",
        "order-worker", "book-service", "analytics-worker"
    ]
)
def test_containers_running(container_name, client):
    containers = client.containers.list()
    names = [container.name for container in containers]
    assert len(names) == 10
    assert container_name in names
