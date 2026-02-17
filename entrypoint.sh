#!/bin/bash

set -e

echo "🚀 Starting Inventario App..."

echo "📁 Creating required directories..."
mkdir -p logs staticfiles media

# Check DATABASE_URL
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL not set"
    exit 1
fi

echo "✅ Database URL configured"

echo "📦 Running migrations..."
python manage.py migrate --noinput

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser in development
if [ "$DEBUG" = "True" ]; then
    echo "👤 Creating development superuser..."
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin123")
    print("Superuser created")
EOF
fi

echo "🌐 Starting Gunicorn..."

exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
