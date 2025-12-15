FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY Module_9/consumer/ .

CMD ["celery", "-A", "worker_service.celery_app", "worker", "--loglevel=info"]