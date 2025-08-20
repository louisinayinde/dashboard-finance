# Use official Playwright image with browsers preinstalled (Ubuntu 22.04 Jammy)
FROM mcr.microsoft.com/playwright/python:v1.46.0-jammy

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    wget \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Playwright and browsers are already included in the base image

# Install Python dependencies
COPY requirements/ requirements/
RUN pip install -r requirements/development.txt

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p logs uploads

# Set permissions (only if shell scripts exist)
RUN if [ -d scripts ] && ls scripts/*.sh >/dev/null 2>&1; then \
      chmod +x scripts/*.sh; \
    fi

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
