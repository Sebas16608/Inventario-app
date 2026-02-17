# 🚀 Quick Start Guide

## Estructura del Proyecto

```
Inventario-app/
├── backend/                 # Django app (core, accounts, inventario)
│   ├── core/               # Django project settings
│   ├── accounts/           # User management
│   ├── inventario/         # Inventory management
│   ├── manage.py
│   ├── requirements.txt
│   ├── entrypoint.sh
│   ├── Dockerfile
│   └── logs/, media/, staticfiles/
│
├── frontend/               # React/Next.js app (vacío por ahora)
│
└── Root files:
    ├── Dockerfile          # Main Docker image
    ├── docker-compose.yml  # Local development
    ├── Procfile           # Render deployment
    ├── render.yaml        # Render config
    └── build.sh           # Build script
```

## 🐳 Docker - Desarrollo Local

### Requisitos
- Docker & Docker Compose
- .env configurado (copiar de .env.example)

### Inicio rápido

```bash
# 1. Copiar variables de entorno
cp .env.example .env

# 2. Editar .env con valores locales
nano .env
# Cambiar: DEBUG=True, ALLOWED_HOSTS, DATABASE_URL

# 3. Iniciar servicios
docker-compose up -d

# 4. Verificar logs
docker-compose logs -f web

# 5. Acceder a la aplicación
http://localhost:8000
```

### Comandos útiles

```bash
# Ver estado
docker-compose ps

# Ejecutar migraciones
docker-compose exec web python backend/manage.py migrate

# Crear superusuario
docker-compose exec web python backend/manage.py createsuperuser

# Recolectar archivos estáticos
docker-compose exec web python backend/manage.py collectstatic --noinput

# Ver logs
docker-compose logs -f web

# Detener servicios
docker-compose down
```

## 🌐 Render.com - Deployment

### Preparación

```bash
# 1. Commitear cambios
git add .
git commit -m "Setup para Render deployment"
git push origin main

# 2. Ir a render.com
# 3. Conectar repositorio GitHub
# 4. Crear Web Service
```

### Configuración en Render

**Build Command:**
```bash
cd backend && pip install -r requirements.txt
```

**Start Command:**
```bash
cd backend && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 3
```

**Environment Variables:**
Ver [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

### Crear Base de Datos

1. Crear servicio PostgreSQL en Render
2. Conectar con Web Service
3. Render proporcionará `DATABASE_URL` automáticamente

## 📋 Checklist Pre-Deploy

- [ ] `DEBUG=False` en producción
- [ ] `SECRET_KEY` generada y segura
- [ ] `ALLOWED_HOSTS` configurado correctamente
- [ ] `DATABASE_URL` apunta a PostgreSQL
- [ ] Variables HTTPS seteadas (`SECURE_SSL_REDIRECT=True`, etc)
- [ ] CORS configurado para dominio
- [ ] Archivos estáticos se sirven correctamente
- [ ] Base de datos migrada

## 🔧 Troubleshooting

### Docker error: "Can't find Dockerfile"
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### DB connection error
- Verificar `DATABASE_URL` está seteada
- Verificar PostgreSQL está corriendo
- Ver logs: `docker-compose logs web`

### Static files no se sirven
```bash
docker-compose exec web python backend/manage.py collectstatic --noinput --clear
```

### Python dependencies error
```bash
docker-compose exec web pip install -r backend/requirements.txt
```

## 📚 Documentación Completa

- [Deployment en Render](RENDER_DEPLOYMENT.md)
- [Documentación General](docs/DOCUMENTACION.md)
- [API Documentation](docs/API.md)
- [JWT Auth](docs/JWT_AUTH.md)
- [Docker](docs/DOCKER.md)

## 🔐 Seguridad

⚠️ **NUNCA**:
- Compartir `.env` con información sensible
- Hacer commit de `.env` a git
- Usar `DEBUG=True` en producción
- Usar contraseñas simples

✅ **HACER**:
- Usar variables de entorno del servidor
- Generar `SECRET_KEY` nueva para cada instalación
- Usar contraseñas fuertes (16+ caracteres)
- Habilitar HTTPS en producción

## ✅ Status

- Backend: ✅ Ready for deployment
- Frontend: ⏳ Coming soon
- Docker: ✅ Configured
- Render: ✅ Ready
