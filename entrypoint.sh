#!/bin/bash
# Wait until the database is ready
echo "Waiting for database..."
until python -c "import psycopg2; psycopg2.connect(dbname='coursedb_yeur', user='coursedb_yeur_user', password='J6ArTCPrukvMHUpevMHaoqLrrILg9UGE', host='dpg-d4jl0pmr433s739fme00-a', port='5432')" > /dev/null 2>&1; do
  echo "Database is unavailable - sleeping"
  sleep 2
done

echo "Database is up - running migrations"
python manage.py migrate

echo "Starting Gunicorn"
gunicorn course_service.wsgi:application --bind 0.0.0.0:10000 --workers 3
