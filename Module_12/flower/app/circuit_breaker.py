from prometheus_client import Gauge, Counter
from aiobreaker import CircuitBreaker

circuit_breaker_state = Gauge(
    "circuit_breaker_state",
    "Состояние Circuit Breaker (0=CLOSED, 1=OPEN, 2=HALF_OPEN)",
    ["breaker_name"]
)

circuit_breaker_failures = Counter(
    "circuit_breaker_failures_total",
    "Общее количество ошибок Circuit Breaker",
    ["breaker_name"]
)

circuit_breaker_successes = Counter(
    "circuit_breaker_successes_total",
    "Общее количество успешных вызовов Circuit Breaker",
    ["breaker_name"]
)


def create_breaker(name: str, failure_threshold: int = 5, timeout: int = 60):
    breaker = CircuitBreaker(
        fail_max=failure_threshold,
        timeout_duration=timeout,
        name=name
    )
    circuit_breaker_state.labels(breaker_name=name).set(0)
    return breaker


db_breaker = create_breaker("database", failure_threshold=5, timeout=60)


async def call_with_breaker(breaker, func, *args, **kwargs):
    state_map = {"CLOSED": 0, "OPEN": 1, "HALF_OPEN": 2}
    breaker_name = breaker.name

    try:
        result = await breaker.call(func, *args, **kwargs)
        circuit_breaker_successes.labels(breaker_name=breaker_name).inc()
        return result
    except Exception:
        circuit_breaker_failures.labels(breaker_name=breaker_name).inc()
        raise
    finally:
        circuit_breaker_state.labels(breaker_name=breaker_name).set(
            state_map.get(breaker.current_state.name, 0)
        )
