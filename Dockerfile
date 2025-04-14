# Use Python 3.8 slim image
FROM python:3.8-slim

# Install cron and procps for debugging
RUN apt-get update && apt-get -y install cron procps

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

# Create and activate virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies in virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create the log file to be able to run tail
RUN touch /var/log/cron.log && \
    chmod 766 /var/log/cron.log

# Create entrypoint script
RUN echo '#!/bin/bash\n\
# Update crontab with environment variable\n\
CRON_SCHEDULE=${CRON_SCHEDULE:-"*/5 * * * *"}\n\
\n\
# Create user crontab file\n\
cat > /tmp/crontab << EOL\n\
SHELL=/bin/bash\n\
PATH=/app/venv/bin:/usr/local/bin:/usr/bin:/bin\n\
PYTHONPATH=/app\n\
${CRON_SCHEDULE} cd /app && /app/venv/bin/python main.py --kafka >> /var/log/cron.log 2>&1\n\
EOL\n\
\n\
# Apply user crontab\n\
crontab /tmp/crontab\n\
\n\
# Start cron as root\n\
/usr/sbin/cron\n\
\n\
# Switch to appuser\n\
exec su - appuser -c "tail -f /var/log/cron.log"' > /entrypoint.sh

RUN chmod +x /entrypoint.sh

# Set ownership of app directory
RUN chown -R appuser:appuser /app

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"] 