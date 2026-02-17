#!/bin/bash
set -o errexit

echo "📦 Installing dependencies..."
cd backend
pip install -r requirements.txt

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "🗄️  Running migrations..."
python manage.py migrate --noinput

echo "✅ Build completed successfully!"
