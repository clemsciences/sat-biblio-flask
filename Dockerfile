# Stage 1: Build dependencies
FROM python:3.11-slim-bookworm AS builder

# Set shell to bash for better support
SHELL ["/bin/bash", "-c"]

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements to leverage Docker cache
COPY requirements.txt .

# Create virtualenv and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# Stage 2: Runtime
FROM python:3.11-slim-bookworm

LABEL authors="Clément Besnier"

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app" \
    FLASK_ENV=production \
    DATA_DIR="/app/data" \
    UPLOAD_DIR="/app/uploads"

WORKDIR /app

# Create necessary directories and user
RUN mkdir -p /app/data /app/uploads && \
    useradd -m -u 1000 satbiblio && \
    chown -m satbiblio:satbiblio /app/data /app/uploads

# Copy virtualenv from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Set permissions
RUN chown -R satbiblio:satbiblio /app

USER satbiblio

# Expose port
EXPOSE 8080

# Use a volume for persistent data
VOLUME ["/app/data", "/app/uploads"]

# Use app_server.py as it seems more tailored for production
CMD ["gunicorn", "--conf", "sat_biblio_server/gunicorn_conf.py", "--bind", "0.0.0.0:8080", "app_server:app"]

HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8080/ || exit 1