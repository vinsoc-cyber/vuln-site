FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd --create-home --uid 10001 app \
    # Install with system-level caching for faster rebuilds
    && pip install --no-cache-dir Flask

WORKDIR /app

COPY --chown=app:app vuln ./vuln

USER app

EXPOSE 1111 1112 1113