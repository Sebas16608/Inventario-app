FROM python:3.13-slim

# Metadatos
LABEL maintainer="Sebastián <asebasrr444@gmail.com>"
LABEL description="Inventario-app - Django REST Framework API"
LABEL version="1.0"

# Evita archivos .pyc y activa logs inmediatos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Agregar backend al PYTHONPATH
ENV PYTHONPATH=/app/backend:$PYTHONPATH

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias
# build-essential: Para compilar extensiones C de Python
# libpq-dev: Para psycopg2 (driver PostgreSQL)
# curl: Para healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (aprovecha Docker cache)
COPY backend/requirements.txt .

# Instalar dependencias Python
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copiar el proyecto completo
COPY . .

# Crear directorios necesarios con permisos adecuados
RUN mkdir -p /app/backend/logs /app/backend/media /app/backend/staticfiles && \
    chmod 755 /app/backend/logs /app/backend/media /app/backend/staticfiles

# Dar permisos al entrypoint
RUN chmod +x /app/backend/entrypoint.sh

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Puerto esperado por la aplicación
EXPOSE 8000

# Healthcheck - verifica que la app está respondiendo
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/admin/ || exit 1

# Establecer working directory para el comando
WORKDIR /app/backend

# Comando final
CMD ["bash", "entrypoint.sh"]
