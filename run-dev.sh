#!/bin/bash

# Script para correr el backend y frontend juntos

echo "🚀 Iniciando Inventario App..."
echo ""

# Verificar si estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Por favor corre este script desde la raíz del proyecto"
    exit 1
fi

# Funcion para limpiar al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    wait $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar Backend
echo "📦 Iniciando Backend (Django)..."
cd backend
source ../.venv/bin/activate 2>/dev/null || source ~/.venv/bin/activate
python manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!
cd ..
sleep 2

# Iniciar Frontend
echo "🎨 Iniciando Frontend (Next.js)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Servicios iniciados correctamente"
echo ""
echo "📱 Backend disponible en: http://localhost:8000"
echo "🖥️  Frontend disponible en: http://localhost:3000"
echo ""
echo "Presiona Ctrl+C para detener los servicios"
echo ""

# Esperar a que los procesos terminen
wait
