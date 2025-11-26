#!/bin/bash
set -e

echo "Waiting for database..."
until python manage.py showmigrations > /dev/null 2>&1; do
    echo "Database not ready, sleeping..."
    sleep 3
done

echo "Removing old migrations..."
# Loop over all apps and delete migration files except __init__.py
for app in $(ls -d */); do
    if [ -d "$app/migrations" ]; then
        find "$app/migrations" -type f -not -name "__init__.py" -delete
    fi
done

echo "Making fresh migrations..."
python manage.py makemigrations --noinput

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn course_service.wsgi:application --bind 0.0.0.0:10000 --workers 3
