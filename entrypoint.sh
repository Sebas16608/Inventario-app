#!/bin/bash

set -e

echo "🚀 Starting Inventario App..."

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL environment variable is not set!"
    echo "💡 Please configure DATABASE_URL in your .env file"
    exit 1
fi

echo "✅ Database URL configured"

# Run migrations
echo "📦 Running database migrations..."
if python manage.py migrate --noinput; then
    echo "✅ Migrations completed successfully"
else
    echo "⚠️  Warning: Migration may have failed (check logs above)"
fi

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist (only in development)
if [ "$DEBUG" = "True" ]; then
    echo "👤 Setting up development superuser..."
    python manage.py shell << 'EOF'
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Development superuser created: admin / admin123")
else:
    print("ℹ️  Superuser already exists")
EOF
