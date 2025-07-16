ARG BUILD_FROM
FROM $BUILD_FROM

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    bashio

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Ensure icon is accessible
RUN if [ -f icon.png ]; then chmod 644 icon.png; fi

# Create non-root user
RUN adduser -D -s /bin/sh app

# Set up permissions and data directory
RUN mkdir -p /data && \
    chown -R app:app /app && \
    chown -R app:app /data && \
    chmod 777 /data

# Switch to app user
USER app

# Expose port
EXPOSE 8124

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8124/health || exit 1

# Start the application
CMD ["python", "app.py"] 