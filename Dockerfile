# syntax=docker/dockerfile:1

FROM python:3.12-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install build dependencies, then dependencies from the lockfile.
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.lock ./
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install -r requirements.lock \
    && /opt/venv/bin/pip install gunicorn==23.0.0


FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    DATABASE_URL="sqlite:////data/db.sqlite3"

# Create a non-root user and the directory for the SQLite database.
RUN groupadd --system app && useradd --system --gid app --home /app app \
    && mkdir -p /app /data \
    && chown app:app /data /app

WORKDIR /app

# Copy only the installed dependencies and application code.
COPY --from=builder /opt/venv /opt/venv
COPY --chown=app:app app ./app

USER app

EXPOSE 8000

# Initialize the database on first boot, then serve the app.
ENTRYPOINT ["sh", "-c", "flask --app app init-db && exec gunicorn --bind 0.0.0.0:8000 --workers 2 'app:create_app()'"]
