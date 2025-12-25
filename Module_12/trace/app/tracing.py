import os
from typing import Optional

from celery import Celery
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor


def setup_zipkin_tracing(
    service_name: str,
    app: Optional[FastAPI] = None,
    celery_app: Optional[Celery] = None
):
    resource = Resource.create({"service.name": service_name})

    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    zipkin_endpoint = os.getenv(
        "ZIPKIN_ENDPOINT",
        "http://zipkin:9411/api/v2/spans"
    )
    zipkin_exporter = ZipkinExporter(endpoint=zipkin_endpoint)

    span_processor = SimpleSpanProcessor(zipkin_exporter)
    provider.add_span_processor(span_processor)

    if app is not None:
        FastAPIInstrumentor.instrument_app(app)
        HTTPXClientInstrumentor().instrument()
        SQLAlchemyInstrumentor().instrument()

    if celery_app is not None:
        CeleryInstrumentor().instrument()
