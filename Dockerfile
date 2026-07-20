# syntax=docker/dockerfile:1

# Stage 1: Build dependencies
FROM python:3.11-slim-bookworm AS builder

# Set shell to bash for better support
SHELL ["/bin/bash", "-c"]

WORKDIR /app

# Keep pip quiet, cache-free and non-interactive during the build
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PATH="/opt/venv/bin:$PATH"

# Install build dependencies (git is needed for the `… @ git+...` dependencies)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# uv can install a project's dependencies straight from pyproject.toml, which pip
# cannot do without building the project (and therefore copying the source).
RUN pip install uv==0.9.21

# Copy only the dependency manifests to leverage Docker cache. `dependencies` is
# static and --no-install-project skips building the app, so uv never needs
# version.txt/README.md/the package itself at this point.
COPY pyproject.toml uv.lock ./

# Install the locked dependencies into /opt/venv (uv creates it).
#   --locked             fail if uv.lock is out of sync with pyproject.toml, so an
#                        image never ships versions nobody committed. NOT --frozen:
#                        that one installs the lock without ever checking it against
#                        pyproject.toml, silently ignoring added dependencies.
#   --no-install-project install dependencies only, not sat-biblio-web itself
# The git dependencies are PEP 508 direct references (not editable), so they land in
# site-packages and are carried over wholesale when /opt/venv moves to the runtime stage.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
RUN uv sync --locked --no-install-project


# Stage 2: Runtime
FROM python:3.11-slim-bookworm

LABEL org.opencontainers.image.authors="Clément Besnier" \
      org.opencontainers.image.title="sat-biblio-server" \
      org.opencontainers.image.description="Flask backend for the Société Archéologique de Touraine library"

# Install runtime dependencies (curl is used by the HEALTHCHECK)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app" \
    FLASK_ENV=production \
    DATA_DIR="/app/data" \
    UPLOAD_DIR="/app/uploads" \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Create a non-root user and the persistent data directories
RUN useradd -m -u 1000 satbiblio && \
    mkdir -p /app/data /app/uploads && \
    chown -R satbiblio:satbiblio /app/data /app/uploads

# Copy virtualenv from builder
COPY --from=builder --chown=satbiblio:satbiblio /opt/venv /opt/venv

# Copy application code with the right ownership in a single layer
COPY --chown=satbiblio:satbiblio . .

USER satbiblio

# Expose port
EXPOSE 8080

# Use a volume for persistent data
VOLUME ["/app/data", "/app/uploads"]

# Use app_server.py as it seems more tailored for production
CMD ["gunicorn", "--conf", "sat_biblio_server/gunicorn_conf.py", "--bind", "0.0.0.0:8080", "app_server:app"]

# The production config sets SERVER_NAME, so Flask only matches requests whose
# Host header equals it — the healthcheck must send that Host or every route 404s.
HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
  CMD curl -f -H "Host: api.satbiblio.clementbesnier.eu" http://localhost:8080/health || exit 1
