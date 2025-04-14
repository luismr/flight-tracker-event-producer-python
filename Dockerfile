# Use Python 3.9 slim image
FROM python:3.9-slim

# Install cron, procps and build dependencies
RUN apt-get update && apt-get -y install \
    cron \
    procps \
    gcc \
    python3-dev \
    python3-venv \
    libffi-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -s /bin/bash appuser

# Set up cron directories and permissions
RUN mkdir -p /var/run/cron && \
    touch /var/run/crond.pid && \
    chown appuser:appuser /var/run/cron /var/run/crond.pid && \
    chmod 755 /var/run/cron && \
    chmod 644 /var/run/crond.pid

# Set working directory
WORKDIR /app
# Set ownership of app directory
RUN chown -R appuser:appuser /app

# Switch to appuser
USER appuser

# Create and activate virtual environment
RUN /usr/bin/python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies in virtual environment
RUN . /app/venv/bin/activate && \ 
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY main.py .
COPY events/ events/
COPY opensky/ opensky/

# Switch to root
USER root

# Copy the docker entrypoint
COPY docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Create the log file to be able to run tail
RUN touch /var/log/cron.log && \
    chmod 766 /var/log/cron.log

# Set entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"] 