#!/bin/bash

# Exit on error
set -e

# Color codes para logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Inventario App...${NC}"

# Validar DATABASE_URL
if [ -z "$DATABASE_URL" ]; then
    echo -e "${RED}❌ ERROR: DATABASE_URL not set${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Database URL configured${NC}"

# Validar PYTHONPATH
if [ -z "$PYTHONPATH" ]; then
    export PYTHONPATH=/app/backend:$PYTHONPATH
    echo -e "${YELLOW}⚠️  PYTHONPATH no configurado, usando default${NC}"
fi

# Crear directorios necesarios
echo -e "${GREEN}📁 Creating required directories...${NC}"
mkdir -p logs staticfiles media

# Aplicar migraciones
echo -e "${GREEN}📦 Running migrations...${NC}"
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo -e "${GREEN}📁 Collecting static files...${NC}"
python manage.py collectstatic --noinput --clear

# Crear superusuario en desarrollo (solo si DEBUG=True)
if [ "$DEBUG" = "True" ]; then
    echo -e "${YELLOW}👤 Creating development superuser...${NC}"
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin123")
    print("✅ Superuser 'admin' created")
else:
    print("ℹ️  Superuser 'admin' already exists")
EOF
fi

# Variables Gunicorn desde ENV (con defaults)
WORKERS=${GUNICORN_WORKERS:-3}
THREADS=${GUNICORN_THREADS:-2}
TIMEOUT=${GUNICORN_TIMEOUT:-60}
MAX_REQUESTS=${GUNICORN_MAX_REQUESTS:-1000}

echo -e "${GREEN}🌐 Starting Gunicorn (workers=$WORKERS, timeout=$TIMEOUT)...${NC}"
echo -e "${GREEN}📊 Access at: http://localhost:8000${NC}"
echo -e "${GREEN}🔐 Admin panel: http://localhost:8000/admin${NC}"

# Ejecutar Gunicorn
exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${WORKERS}" \
    --threads "${THREADS}" \
    --worker-class gthread \
    --worker-tmp-dir /dev/shm \
    --timeout "${TIMEOUT}" \
    --max-requests "${MAX_REQUESTS}" \
    --max-requests-jitter 50 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
