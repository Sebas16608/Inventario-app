# 🚀 Guía de Deployment con Docker

## Requisitos Previos

- Docker y Docker Compose instalados
- Cuenta en Neon Database (https://neon.tech)
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

# Clonar repositorio
cd /home/usuario
git clone https://github.com/Sebas16608/Inventario-app.git
cd Inventario-app
```

### 2. **Configurar Variables de Entorno**

```bash
# Copiar archivo de producción
cp .env.production .env

# Editar con tus valores
nano .env
```

**Variables a editar en `.env`:**

```env
# Generar SECRET_KEY seguro:
python3 -c "import secrets; print(secrets.token_urlsafe(50))"

SECRET_KEY=<tu-secret-key>
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

# Database Neon (ya viene configurada)
DATABASE_URL=postgresql://neondb_owner:npg_1JfSvbaj9dFm@ep-rough-haze-aiy3227g-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

# HTTPS
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com

# CORS
CORS_ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
```

### 3. **Certificados SSL (Opcional pero Recomendado)**

```bash
# Crear directorio para SSL
mkdir -p ssl

# Opción A: Usar Let's Encrypt con Certbot
sudo apt install certbot python3-certbot-nginx -y

# Generar certificado
sudo certbot certonly --standalone -d tu-dominio.com -d www.tu-dominio.com

# Copiar certificados
sudo cp /etc/letsencrypt/live/tu-dominio.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/tu-dominio.com/privkey.pem ssl/key.pem
sudo chown $USER:$USER ssl/*.pem

# Opción B: Auto-generar certificado autofirmado (desarrollo)
openssl req -x509 -newkey rsa:4096 -nodes -out ssl/cert.pem -keyout ssl/key.pem -days 365
```

### 4. **Construir y Ejecutar Contenedores**

```bash
# Construcción de imágenes
docker-compose build

# Ejecutar en background (con BD externa)
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Ver estado
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
- [Django Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
- [Nginx Documentation](https://nginx.org/en/docs/)
