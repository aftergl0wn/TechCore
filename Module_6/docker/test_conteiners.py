import docker
import pytest


@pytest.fixture
def client():
    return docker.from_env()


@pytest.mark.parametrize(
    "container_name", ["module_6-redis-1", "module_6-mongo-1"]
)
def test_containers_running(container_name, client):
    containers = client.containers.list()
    names = [container.name for container in containers]
    assert container_name in names
