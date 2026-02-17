# 🚀 DEPLOYMENT CHECKLIST

## ✅ Backend Refactorization - COMPLETADO

- [x] Estructura reorganizada: `backend/` + `frontend/`
- [x] Todos los módulos Django en `backend/` (core, accounts, inventario)
- [x] `manage.py` en `backend/`
- [x] `requirements.txt` en `backend/`
- [x] `entrypoint.sh` en `backend/`
- [x] `API.py` movido a `backend/`
- [x] Directorios de almacenamiento en `backend/` (logs, media, staticfiles)

## 🐳 Docker Configuration - COMPLETADO

- [x] `Dockerfile` en raíz (apunta a `backend/`)
- [x] `docker-compose.yml` actualizado
- [x] `PYTHONPATH=/app/backend` configurado
- [x] `.dockerignore` creado
- [x] Volumes correctamente mapeados
- [x] Healthchecks definidos
- [x] Working directory correcto

## 🌐 Render.com Configuration - COMPLETADO

- [x] `Procfile` creado con comandos correctos
- [x] `runtime.txt` con Python 3.13.1
- [x] `render.yaml` con configuración completa
- [x] `build.sh` script de build
- [x] Release commands para migraciones
- [x] Documentación RENDER_DEPLOYMENT.md

## 📝 Documentación - COMPLETADO

- [x] `QUICKSTART.md` - Guía rápida
- [x] `RENDER_DEPLOYMENT.md` - Guía Render
- [x] `PROJECT_STRUCTURE.md` - Estructura completa
- [x] `.env.example` - Variables documentadas
- [x] `verify-setup.sh` - Script de verificación

## 🔐 Seguridad - COMPLETADO

- [x] DEBUG=False para producción
- [x] SECURE_SSL_REDIRECT configurado
- [x] SESSION_COOKIE_SECURE habilitado
- [x] CSRF_COOKIE_SECURE habilitado
- [x] HSTS headers
- [x] X-Frame-Options
- [x] CORS configurado
- [x] .gitignore actualizado

---

## 📋 PRE-DEPLOYMENT (Pasos a ejecutar)

### 1. Configuración Local

```bash
# Copiar variables de entorno
cp .env.example .env

# Editar .env con valores locales
nano .env

# Cambiar estos valores en .env:
# DEBUG=True (para desarrollo)
# ALLOWED_HOSTS=localhost,127.0.0.1
# DATABASE_URL=postgresql://user:pass@localhost:5432/db
```

### 2. Probar con Docker Localmente

```bash
# Verificar estructura
./verify-setup.sh

# Construir imagen
docker-compose build

# Iniciar servicios
docker-compose up -d

# Verificar que funciona
curl http://localhost:8000/admin/

# Ver logs
docker-compose logs -f web
```

### 3. Preparar para Git

```bash
# Asegurar que .env NO está en git
echo ".env" >> .gitignore

# Verificar estado
git status

# Agregar cambios
git add .

# Commit
git commit -m "Refactor: Reorganizar proyecto con backend/ y preparar para Render deployment"

# Push
git push origin main
```

### 4. Deploy en Render

```bash
# Ir a https://render.com
# 1. Clickear "New +" -> "Web Service"
# 2. Conectar repositorio GitHub
# 3. Nombre: inventario-app
# 4. Build Command:
#    cd backend && pip install -r requirements.txt
# 5. Start Command:
#    cd backend && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 3
# 6. Environment Variables (ver .env.example)
# 7. Deploy
```

### 5. Configurar Base de Datos

```bash
# En Render Dashboard:
# 1. Crear nuevo servicio PostgreSQL
# 2. Nombrar: inventario-db
# 3. Conectar con web service
# 4. Render proporcionará DATABASE_URL automáticamente
```

### 6. Ejecutar Migraciones (Primer Deploy)

```bash
# Opción A: Automático (Procfile release command)
# Render ejecuta automáticamente: 
# cd backend && python manage.py migrate --noinput

# Opción B: Manual desde Shell tú Render
# cd backend
# python manage.py migrate --noinput
# python manage.py createsuperuser
# python manage.py collectstatic --noinput
```

---

## 🎯 Post-Deployment

- [ ] Verificar que app está online: `yourdomain.onrender.com`
- [ ] Admin accessible: `yourdomain.onrender.com/admin`
- [ ] Monitorear logs en Render Dashboard
- [ ] Configurar dominio personalizado (si aplica)
- [ ] Configurar SSL automático
- [ ] Configurar backups de BD
- [ ] Setup monitoring/alertas

---

## 🔍 Testing

### Local
```bash
# Verificación
./verify-setup.sh

# Migraciones
python manage.py migrate --help

# Testing
python manage.py test
```

### Docker
```bash
# Logs
docker-compose logs -f web

# Shell Django
docker-compose exec web backend/manage.py shell

# Crear superuser
docker-compose exec web python backend/manage.py createsuperuser
```

### Verificación en Render
```
Dashboard -> Web Service -> Logs
Buscar: "Starting Gunicorn" (indica que inició correctamente)
```

---

## 📞 Troubleshooting

| Problema | Solución |
|----------|----------|
| "No module named core" | PYTHONPATH debe ser `/app/backend` ✅ Ya configurado |
| DB connection error | Revisar DATABASE_URL está seteada ✅ |
| Static files no se sirven | `python manage.py collectstatic` ✅ |
| Port 8000 en uso | `docker-compose down` o usar otro puerto |
| Migraciones fallan | Ver logs: `docker-compose logs web` |

---

## ✨ Status Final

```
✅ Backend refactorizado
✅ Docker configurado
✅ Render listo
✅ Documentación completa
✅ Scripts de verificación
✅ Seguridad configurada
```

**Proyecto listo para deployment en Render.com** 🚀

---

**Última actualización**: 17 de febrero 2026
**Backend versión**: Django 5.1.5
**Python versión**: 3.13.1
