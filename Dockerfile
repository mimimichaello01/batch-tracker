FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt update -y && \
    apt install -y gcc libpq-dev && \
    pip install --upgrade pip && \
    pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

COPY ./src /app
