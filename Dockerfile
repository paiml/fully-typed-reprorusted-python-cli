# fully-typed-reprorusted-python-cli - Reproducible Build Environment
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential git curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml .
RUN uv sync

COPY . .
RUN uv sync

CMD ["uv", "run", "pytest", "--cov-fail-under=95", "-v"]
