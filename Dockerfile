# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-slim AS builder

LABEL maintainer="Terada Kousuke <company@cor-jp.com>"
LABEL description="GPUStack Local LLM Chatbot Docker Image"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Copy requirements files
COPY app/requirements.txt /app/app/requirements.txt

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip wheel \
    && pip install gpustack \
    && pip install -r app/requirements.txt

# Multi-platform final image
FROM --platform=$TARGETPLATFORM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Make scripts executable
RUN chmod +x /app/docker-entrypoint.sh \
    && chmod +x /app/scripts/deploy_small_model.py

# Download GPUStack tools
RUN gpustack download-tools

# Create necessary directories
RUN mkdir -p /var/lib/gpustack \
    && mkdir -p /root/.gpustack

# Expose ports
# 80: GPUStack Playground UI
# 8501: Streamlit app
EXPOSE 80 8501

# Set entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"]
