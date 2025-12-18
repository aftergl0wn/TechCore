import docker
import pytest


@pytest.fixture
def client():
    return docker.from_env()
