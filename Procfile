web: cd backend && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --worker-class sync --max-requests 1000 --max-requests-jitter 50 --timeout 60 --access-logfile - --error-logfile - --log-level info
release: cd backend && python manage.py migrate --noinput && python manage.py collectstatic --noinput --clear && echo "✅ Migraciones completadas"
