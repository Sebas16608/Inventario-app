# 🚀 Guía de Deployment con Docker

## Requisitos Previos

- Docker y Docker Compose instalados
- Base de datos PostgreSQL externa (ej: Neon Database, AWS RDS, etc.)
- Dominio configurado (para producción)
- Certificado SSL (para HTTPS en producción)

---

## 📋 Pasos para el Deployment

### 1. **Preparar el Servidor**

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Agregar usuario a grupo docker (opcional)
sudo usermod -aG docker $USER

# Clonar repositorio
cd /home/usuario
git clone https://github.com/Sebas16608/Inventario-app.git
cd Inventario-app
```

### 2. **Preparar Variables de Entorno**

⚠️ **IMPORTANTE**: Nunca expongas el `.env` en el repositorio

```bash
# Crear archivo de configuración local (NO se seguirá en git)
touch .env

# Editar con tus valores
nano .env
```

**Variables requeridas en `.env`:**

```env
# Django Configuration
DEBUG=False
SECRET_KEY=tu-secret-key-super-seguro-aleatorio

# Hosts permitidos
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,ip-del-servidor

# DATABASE - URL de Neon o tu proveedor externo
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_bd?sslmode=require

# HTTPS Security (cambiar a True en producción)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com

# CORS
CORS_ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com,https://app.tu-dominio.com

# Logging
DJANGO_LOG_LEVEL=WARNING
```

**Generar un SECRET_KEY seguro:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 3. **Certificados SSL (Recomendado)**

```bash
# Crear directorio para SSL
mkdir -p ssl

# Opción A: Usar Let's Encrypt con Certbot
sudo apt install certbot python3-certbot-nginx -y

# Generar certificado
sudo certbot certonly --standalone -d tu-dominio.com -d www.tu-dominio.com

# Copiar certificados al directorio del proyecto
sudo cp /etc/letsencrypt/live/tu-dominio.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/tu-dominio.com/privkey.pem ssl/key.pem
sudo chmod 644 ssl/*

# Opción B: Generar certificado autofirmado (solo desarrollo)
openssl req -x509 -newkey rsa:4096 -nodes -out ssl/cert.pem -keyout ssl/key.pem -days 365
```

### 4. **Construir e Iniciar la Aplicación**

```bash
# Construir la imagen Docker
docker-compose build

# Ejecutar en background (solo Django)
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f web

# Verificar estado de los contenedores
docker-compose ps

# Detener los contenedores
docker-compose down
```

### 5. **Con Nginx (Producción)**

Si deseas usar Nginx como reverse proxy:

```bash
# Iniciar con Nginx
docker-compose --profile production up -d

# Ver logs
docker-compose logs -f nginx

# Detener
docker-compose --profile production down
```

---

## 📊 Estructura de Contenedores

### Configuración por Defecto (Desarrollo/Testing)

```
┌─────────────────┐
│   Tu Máquina    │
│                 │
│  ┌───────────┐  │
│  │  Django   │←──── Port 8000
│  │ (Gunicorn)│  │
│  └─────┬─────┘  │
│        │        │
│        ▼        │
│  ┌───────────┐  │
│  │ Neon/RDS  │  │
│  │   (DB)    │  │
│  └───────────┘  │
└─────────────────┘
```

### Configuración con Nginx (Producción)

```
┌──────────────────────────┐
│      Tu Máquina          │
│                          │
│  ┌──────────────────┐   │
│  │  Nginx (Port 80) │←──── HTTP
│  │ (Reverse Proxy)  │   │
│  └────────┬─────────┘   │
│           ▼              │
│  ┌──────────────────┐   │
│  │  Django:8000     │   │
│  │  (Gunicorn)      │   │
│  └────────┬─────────┘   │
│           ▼              │
│  ┌──────────────────┐   │
│  │ Neon/RDS (DB)    │   │
│  └──────────────────┘   │
└──────────────────────────┘
```

---

## 🔧 Comandos Útiles

```bash
# Ver logs de la aplicación
docker-compose logs -f web

# Acceder a la consola Django dentro del contenedor
docker-compose exec web python manage.py shell

# Crear un superusuario manualmente
docker-compose exec web python manage.py createsuperuser

# Ejecutar migraciones manualmente
docker-compose exec web python manage.py migrate

# Recolectar archivos estáticos manualmente
docker-compose exec web python manage.py collectstatic --noinput

# Reiniciar solo el servicio web
docker-compose restart web

# Reconstruir la imagen (después de actualizar requirements.txt)
docker-compose build --no-cache

# Ver estado detallado
docker-compose ps -a
docker stats
```

---

## 🚨 Troubleshooting

### Error: "DATABASE_URL is not set"

```
Solución: Asegúrate de que DATABASE_URL esté definido en el archivo .env
```

### Error: "Connection refused" a la base de datos

```
- Verifica que DATABASE_URL sea correcto
- Comprueba que el servidor de BD está en línea y accesible
- Revisa que no haya firewall bloqueando la connexión
- Comprueba los logs: docker-compose logs web
```

### Error: "Static files not found"

```
Solución: Ejecuta
docker-compose exec web python manage.py collectstatic --noinput --clear
```

### Verificar que la aplicación esté funcionando

```bash
# Revisar logs
docker-compose logs web

# Acceder a http://localhost:8000/admin (debe mostrar login)

# Verificar healthcheck
docker inspect inventario_app | grep -A 5 Health
```

---

## 🔒 Seguridad en Producción

1. ✅ `DEBUG=False` en las variables
2. ✅ `SECURE_SSL_REDIRECT=True` para forzar HTTPS
3. ✅ Cookie segura: `SESSION_COOKIE_SECURE=True`
4. ✅ CSRF seguro: `CSRF_COOKIE_SECURE=True`
5. ✅ Certificado SSL actualizado
6. ✅ Backup regular de la BD
7. ✅ Monitoreo de logs
8. ✅ Database URL seguro y no expuesto

---

## 📈 Escalado

Para mayores cargas, considera:

```yaml
# docker-compose.yml - Aumentar workers
command: gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 8
```

O usando un process manager como Supervisor o systemd.

---

## 📝 Notas

- La base de datos DEBE ser externa (Neon, AWS RDS, etc.)
- Los logs se guardan en `/app/logs/django.log`
- Los archivos estáticos se almacenan en `/app/staticfiles`
- Los archivos media se almacenan en `/app/media`

docker-compose ps
```

### 5. **Ejecutar Migraciones**

```bash
# Las migraciones se ejecutan automáticamente en el entrypoint.sh
# Pero si necesitas ejecutarlas manualmente:
docker-compose exec web python manage.py migrate

# Crear superadmin (opcional)
docker-compose exec web python manage.py createsuperuser
```

### 6. **Recolectar Static Files**

```bash
# También se ejecuta automáticamente, pero si necesitas:
docker-compose exec web python manage.py collectstatic --noinput
```

---

## 📊 Monitoreo

### Ver logs en tiempo real

```bash
# Todos los servicios
docker-compose logs -f

# Solo Django
docker-compose logs -f web

# Solo Nginx
docker-compose logs -f nginx
```

### Verificar estado de contenedores

```bash
docker-compose ps
```

### Acceder al contenedor

```bash
docker-compose exec web bash
```

---

## 🔄 Actualizaciones

### Actualizar el código

```bash
git pull origin main
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
```

### Limpiar volúmenes (destructivo)

```bash
# Eliminar todos los volúmenes (CUIDADO: borra la BD local)
docker-compose down -v
```

---

## 🛠️ Troubleshooting

### Error: "connection refused"

```bash
# Verificar que la BD Neon esté disponible
# Probar conexión manual:
psql postgresql://neondb_owner:npg_1JfSvbaj9dFm@ep-rough-haze-aiy3227g-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### Error: "static files not found"

```bash
# Recolectar static files
docker-compose exec web python manage.py collectstatic --noinput

# Reiniciar nginx
docker-compose restart nginx
```

### Error: "permission denied"

```bash
# Cambiar permisos si es necesario
sudo chown -R $USER:$USER /ruta/del/proyecto
```

---

## 📈 Escalado

### Aumentar workers de Gunicorn

En `docker-compose.yml`, editar línea de comando de `web`:

```bash
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 8  # Aumentar de 4 a 8
```

### Usar Redis para cache/sessions

```bash
# Editar requirements.txt
redis==4.5.4
django-redis==5.2.0

# Configurar en settings.py
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
    }
}
```

---

## 🔒 Seguridad

✅ **Checklist de Producción:**

- [ ] SECRET_KEY cambiada
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS configurado
- [ ] HTTPS habilitado (SECURE_SSL_REDIRECT=True)
- [ ] Certificado SSL válido (no autofirmado)
- [ ] Database URL verificada
- [ ] CORS_ALLOWED_ORIGINS restringido
- [ ] CSRF_TRUSTED_ORIGINS configurado
- [ ] Backups configurados
- [ ] Monitoreo de logs activo
- [ ] Firewall configurado (solo puertos 80, 443)

---

## 📞 Soporte

Para problemas o preguntas, contactar a: sebastian@example.com

---

## 🔗 Enlaces Útiles

- [Docker Documentation](https://docs.docker.com)
- [Neon Database Docs](https://neon.tech/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)
- [Nginx Documentation](https://nginx.org/en/docs/)
