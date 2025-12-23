import os
from typing import Optional

from celery import Celery
from fastapi import FastAPI
from opentelemetry import metrics, trace
from opentelemetry.metrics import Counter
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from prometheus_client import REGISTRY, generate_latest


_book_count: Optional[Counter] = None


def setup_zipkin_tracing(
    service_name: str,
    app: Optional[FastAPI] = None,
    celery_app: Optional[Celery] = None
):
    resource = Resource.create({"service.name": service_name})

    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)

    span_processor = SimpleSpanProcessor(otlp_exporter)
    provider.add_span_processor(span_processor)
    metrics.set_meter_provider(
        MeterProvider(
            resource=resource,
            metric_readers=[PrometheusMetricReader()]
        )
    )
    global _book_counter
    global_meter_provider = metrics.get_meter_provider()
    meter = global_meter_provider.get_meter("book-service")
    _book_counter = meter.create_counter(
        "books_created_total",
        description="Общее количество созданных книг"
    )
    PymongoInstrumentor().instrument()
    if app is not None:
        FastAPIInstrumentor.instrument_app(app)
        HTTPXClientInstrumentor().instrument()
        SQLAlchemyInstrumentor().instrument()

    if celery_app is not None:
        CeleryInstrumentor().instrument()


def get_prometheus_metrics() -> str:
    return generate_latest(REGISTRY).decode("utf-8")


def get_book_counter() -> Optional[Counter]:
    return _book_counter
