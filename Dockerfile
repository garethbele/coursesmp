# Use official Python slim image
FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose port (Render maps $PORT automatically)
EXPOSE 10000

# Run migrations at container start, then start Gunicorn
CMD python manage.py migrate && gunicorn course_service.wsgi:application --bind 0.0.0.0:10000 --workers 3
