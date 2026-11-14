
# Stage 1: Install dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project


# Stage 2: Run the application
FROM python:3.11-slim

WORKDIR /app

# Create a non-root user
RUN groupadd --system appgroup && \
    useradd --system --gid appgroup appuser

# Copy installed dependencies
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY api/ ./api/
COPY migrations/ ./migrations/
COPY alembic.ini ./

# Set permissions
RUN chown -R appuser:appgroup /app

# Run as non-root user
USER appuser

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
