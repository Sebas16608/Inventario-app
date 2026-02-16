#!/bin/bash

set -e

echo "🚀 Starting Inventario App..."

# Wait for database to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "✅ PostgreSQL is ready!"

# Run migrations
echo "📦 Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist (optional - only for development)
if [ "$DEBUG" = "True" ]; then
  echo "👤 Creating default superuser..."
  python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Superuser created: admin / admin123")
else:
    print("ℹ️ Superuser already exists")
END
fi

echo "✨ Starting Django application with Gunicorn..."
exec "$@"
