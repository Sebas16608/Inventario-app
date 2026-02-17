#!/bin/bash
# Verification script para asegurar que el proyecto está listo para deployment

echo "🔍 Verificando estructura del proyecto..."
echo ""

# Array de archivos que deben existir
FILES=(
    "backend/core/settings.py"
    "backend/core/wsgi.py"
    "backend/accounts/models.py"
    "backend/inventario/models/product.py"
    "backend/manage.py"
    "backend/requirements.txt"
    "backend/entrypoint.sh"
    "backend/Dockerfile"
    "Dockerfile"
    "docker-compose.yml"
    "Procfile"
    "runtime.txt"
    "build.sh"
    ".env.example"
    "render.yaml"
    "RENDER_DEPLOYMENT.md"
    "QUICKSTART.md"
)

# Verificar cada archivo
MISSING=0
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ FALTA: $file"
        ((MISSING++))
    fi
done

echo ""
echo "------- CONFIGURACIÓN CRÍTICA -------"
echo ""

# Verificar Dockerfile en root
if grep -q "PYTHONPATH=/app/backend" Dockerfile; then
    echo "✅ Dockerfile: PYTHONPATH configurado"
else
    echo "❌ Dockerfile: PYTHONPATH no configurado"
fi

# Verificar docker-compose PYTHONPATH
if grep -q "PYTHONPATH: /app/backend" docker-compose.yml; then
    echo "✅ docker-compose.yml: PYTHONPATH configurado"
else
    echo "⚠️  docker-compose.yml: PYTHONPATH check"
fi

# Verificar Procfile
if grep -q "cd backend &&" Procfile; then
    echo "✅ Procfile: Cambio de directorio configurado"
else
    echo "❌ Procfile: Debe incluir 'cd backend &&'"
fi

# Verificar requirements.txt en backend
if [ -f "backend/requirements.txt" ]; then
    if grep -q "Django" backend/requirements.txt; then
        echo "✅ requirements.txt: Django presente"
    fi
    if grep -q "gunicorn" backend/requirements.txt; then
        echo "✅ requirements.txt: gunicorn presente"
    fi
fi

# Verificar settings.py
if [ -f "backend/core/settings.py" ]; then
    if grep -q "INSTALLED_APPS" backend/core/settings.py; then
        echo "✅ settings.py: INSTALLED_APPS presente"
    fi
fi

echo ""
echo "------- RESUMEN -------"
if [ $MISSING -eq 0 ]; then
    echo "✅ Todos los archivos están presentes"
    echo "✅ Proyecto listo para deployment"
else
    echo "❌ $MISSING archivo(s) faltante(s)"
    echo "⚠️  Revisa los archivos faltantes antes de deployar"
fi

echo ""
echo "🚀 Próximos pasos:"
echo "  1. Verificar .env con valores correctos"
echo "  2. Hacer: git push origin main"
echo "  3. Deploy en Render.com"
echo ""
