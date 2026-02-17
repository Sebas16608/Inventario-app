# 🚀 Deployment Guide - Render.com

## Estructura del Proyecto

```
Inventario-app/
├── backend/
│   ├── core/
│   ├── accounts/
│   ├── inventario/
│   ├── manage.py
│   ├── entrypoint.sh
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
├── Dockerfile
├── docker-compose.yml
├── Procfile
├── render.yaml
├── .env.example
└── README.md
```

## Deployment en Render

### 1. Preparación

```bash
# Asegúrate de que todo esté en git
git add .
git commit -m "Preparado para deployment en Render"
git push origin main
```

### 2. Crear Servicio en Render

1. Ve a [render.com](https://render.com)
2. Conecta tu repositorio de GitHub
3. Crea un nuevo "Web Service"
4. Selecciona:
   - **Name**: inventario-app
   - **Environment**: Python 3
   - **Build Command**: 
     ```
     cd backend && pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```
     cd backend && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 3
     ```

### 3. Variables de Entorno

Agrega estas variables en Render Dashboard:

```
DEBUG=False
SECRET_KEY=<generate-secure-key>
ALLOWED_HOSTS=yourdomain.onrender.com,yourdomain.com
DATABASE_URL=<PostgreSQL URL from Render>
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
CORS_ALLOWED_ORIGINS=https://yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
```

### 4. Crear Base de Datos PostgreSQL

1. En Render Dashboard, crea un nuevo servicio "PostgreSQL"
2. Conecta el servicio PostgreSQL con tu Web Service
3. Render proporcionará `DATABASE_URL` automáticamente

### 5. Ejecutar Migraciones

Después del primer deploy, ejecuta:

```bash
# En Render Shell (desde Dashboard):
cd backend
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

O usa el comando `release` en Procfile (automático):
```
release: cd backend && python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

## Deployment Local con Docker

### Desarrollo

```bash
docker-compose up -d
# Accede a: http://localhost:8000
```

### Producción

```bash
docker-compose --profile production up -d
# Nginx estará en: http://localhost
```

## Troubleshooting

### Error: "No module named 'core'"

**Solución**: Asegúrate que `PYTHONPATH=/app/backend` esté configurado.

### Error: "Connection refused" en base de datos

**Verificar**:
1. Que `DATABASE_URL` esté correctamente seteada
2. Que Render PostgreSQL service esté disponible

### Static files no se sirven

```bash
cd backend
python manage.py collectstatic --noinput --clear
```

### Logs en Render

```bash
# Ver logs en tiempo real
# En Render Dashboard -> Web Service -> Logs
# O usar tail desde consola
tail -f backend/logs/django.log
```

## Healthcheck

Render verifica automáticamente: `GET /admin/`

Si ves errores, verifica que Django esté corriendo correctamente.

## Generador de Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

## Secure Settings para Producción

✅ SECURE_SSL_REDIRECT = True
✅ SESSION_COOKIE_SECURE = True
✅ CSRF_COOKIE_SECURE = True
✅ SECURE_HSTS_SECONDS = 31536000 (1 año)
✅ DEBUG = False

## URLs Útiles

- Aplicación: https://yourdomain.onrender.com
- Admin: https://yourdomain.onrender.com/admin
- API: https://yourdomain.onrender.com/api

## Próximos Pasos

- [ ] Configurar dominio personalizado
- [ ] Configurar SSL automático
- [ ] Configurar monitoring/alertas
- [ ] Configurar backups automáticos de BD
- [ ] Agregar email transaccional
