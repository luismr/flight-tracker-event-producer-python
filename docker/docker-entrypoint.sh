#!/bin/bash -x
# Update crontab with environment variable
CRON_SCHEDULE=${CRON_SCHEDULE:-"*/5 * * * *"}

# Export all environment variables to a file
env | grep -v "HOSTNAME\\|HOME\\|PATH\\|TERM" > /app/.env

# Create user crontab file
cat > /tmp/crontab << EOL
SHELL=/bin/sh
PATH=/app/venv/bin:/usr/local/bin:/usr/bin:/bin
PYTHONPATH=/app
${CRON_SCHEDULE} su - appuser -c "cd /app && . /app/.env && . /app/venv/bin/activate && python main.py --kafka >> /var/log/cron.log 2>&1"
EOL

# Apply user crontab
crontab /tmp/crontab

# Set proper permissions for env file
chown appuser:appuser /app/.env
chmod 600 /app/.env

# Start cron as root
/usr/sbin/cron

# Switch to appuser
exec tail -f /var/log/cron.log