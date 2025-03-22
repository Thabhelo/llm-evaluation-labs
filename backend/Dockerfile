FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /var/log && \
    chown -R appuser:appuser /var/log && \
    mkdir -p /var/run && \
    chown -R appuser:appuser /var/run

FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy user from builder
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /home/appuser /home/appuser

# Copy application code
COPY . .
COPY supervisor.conf /etc/supervisor/conf.d/supervisord.conf

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose ports
EXPOSE 8000 5555

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"] 