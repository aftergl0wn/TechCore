import pytest


@pytest.mark.parametrize(
    "container_name",
    ["db", "redis", "rabbitmq", "zipkin", "zookeeper", "mongo", "kafka"]
)
def test_containers_running(container_name, client):
    containers = client.containers.list()
    names = [container.name for container in containers]
    assert len(names) == 7
    assert container_name in names
