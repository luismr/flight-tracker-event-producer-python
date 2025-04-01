# Use Python 3.8 slim image
FROM python:3.8-slim

# Install cron
RUN apt-get update && apt-get -y install cron

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Create crontab file
RUN echo "SHELL=/bin/bash" > /etc/cron.d/flight-tracker-cron
RUN echo "PATH=/usr/local/bin:/usr/bin:/bin" >> /etc/cron.d/flight-tracker-cron
RUN echo "PYTHONPATH=/app" >> /etc/cron.d/flight-tracker-cron
RUN echo "*/5 * * * * cd /app && python main.py --kafka >> /var/log/cron.log 2>&1" >> /etc/cron.d/flight-tracker-cron

# Give execution rights to the crontab file
RUN chmod 0644 /etc/cron.d/flight-tracker-cron

# Apply cron job
RUN crontab /etc/cron.d/flight-tracker-cron

# Create entrypoint script
RUN echo '#!/bin/bash\n\
# Update crontab with environment variable\n\
CRON_SCHEDULE=${CRON_SCHEDULE:-"*/5 * * * *"}\n\
\n\
# Create new crontab file\n\
cat > /etc/cron.d/flight-tracker-cron << EOL\n\
SHELL=/bin/bash\n\
PATH=/usr/local/bin:/usr/bin:/bin\n\
PYTHONPATH=/app\n\
${CRON_SCHEDULE} cd /app && python main.py --kafka >> /var/log/cron.log 2>&1\n\
EOL\n\
\n\
# Apply cron job\n\
crontab /etc/cron.d/flight-tracker-cron\n\
\n\
# Run cron in the foreground\n\
exec cron -f' > /entrypoint.sh

RUN chmod +x /entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"] 