def test_containers_running(client):
    containers = client.containers.list()
    names = [container.name for container in containers]
    assert "traefik" in names
