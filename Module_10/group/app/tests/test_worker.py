import subprocess


def test_four_workers():
    result = subprocess.run(
        ["docker-compose", "ps", "-q", "analytics-worker"],
        capture_output=True,
        text=True,
        check=True,
    )
    containers = [line for line in result.stdout.splitlines() if line.strip()]
    assert len(containers) == 4
