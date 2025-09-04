# notifications-service/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Run Celery worker by default
CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info"]
