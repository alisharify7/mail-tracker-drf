#!/bin/bash

set -e

echo "📦 Applying database migrations..."
if [ "$DJANGO_ENV" != "production" ]; then
  echo "⚙️  Running makemigrations (DEV mode)"
  python manage.py makemigrations --noinput
fi
python manage.py migrate --noinput

python manage.py runserver 0.0.0.0:8000

#echo "🚀 Starting Gunicorn..."
#exec gunicorn core.wsgi:application \
#    --bind 0.0.0.0:8000 \
#    --workers 4 \
#    --timeout 120 \
#    --log-level info \
#    --access-logfile - \
#    --error-logfile -
