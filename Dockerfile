# Multi-stage production Dockerfile for ResearchCore AI

# Stage 1: Build Dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final Runtime Image
FROM python:3.11-slim

WORKDIR /app

# Non-root security user
RUN groupadd -r research && useradd --no-log-init -r -g research research

# Copy dependencies from builder
COPY --from=builder /root/.local /home/research/.local
ENV PATH=/home/research/.local/bin:$PATH
ENV PYTHONPATH=/app

# Copy application source
COPY . /app

# Ensure correct permissions
RUN mkdir -p /app/outputs && chown -R research:research /app

USER research

EXPOSE 8000 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

CMD ["python", "-m", "uvicorn", "src.research_system.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
