# 🐳 Docker - Guía Rápida

Esta guía está diseñada para trabajar con **base de datos externa** (como Neon, AWS RDS, etc.).

## ⚡ Inicio Rápido

### 1. Preparar Variables de Entorno

```bash
# Crear archivo .env (NO se seguirá en git)
touch .env

# Editar con tu configuración
nano .env
```

**Variables mínimas requeridas:**
```env
SECRET_KEY=tu-secret-key-aleatorio-super-seguro
DEBUG=False
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_bd
ALLOWED_HOSTS=localhost,127.0.0.1,tu-dominio.com
```

**Para obtener un SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 2. Construir la Imagen

```bash
docker-compose build
```

### 3. Ejecutar la Aplicación

```bash
# Ejecutar en background
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f web

# Detener
docker-compose down
```

### 4. Acceder a la Aplicación

```
http://localhost:8000/admin
```

Usuario por defecto (en DEBUG=True):
- Username: `admin`
- Password: `admin123`

---

## 📁 Estructura

```
inventario-app/
├── Dockerfile          # Configuración de la imagen
├── docker-compose.yml  # Orchestración de contenedores
├── entrypoint.sh       # Script de inicio
├── .env               # Variables de entorno (crear manualmente)
└── .dockerignore      # Archivos a ignorar en la imagen
```

---

## 🔧 Comandos Comunes

| Comando | Descripción |
|---------|-------------|
| `docker-compose build` | Construir la imagen |
| `docker-compose up -d` | Ejecutar en background |
| `docker-compose logs -f web` | Ver logs |
| `docker-compose down` | Detener contenedores |
| `docker-compose ps` | Ver estado |
| `docker-compose exec web bash` | Acceder a la consola del contenedor |
| `docker-compose restart web` | Reiniciar la aplicación |

---

## 📊 Con Nginx (Producción)

Si deseas usar Nginx como reverse proxy:

```bash
# Crear directorio para certificados SSL
mkdir -p ssl

# Iniciar con Nginx
docker-compose --profile production up -d

# Ver logs
docker-compose logs -f nginx

# Detener
docker-compose --profile production down
```

---

## 🚨 Troubleshooting

### "DATABASE_URL is not set"
- Verifica que `DATABASE_URL` esté en `.env`
- Reinicia el contenedor: `docker-compose restart web`

### "Connection refused" a la base de datos
- Revisa que la URL de BD sea correcta
- Verifica que el servidor de BD esté en línea
- Comprueba el firewall

### "Static files not found"
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Ver logs detallados
```bash
docker-compose logs web | tail -100
```

---

## 📝 Variables de Entorno Disponibles

```env
# Django
DEBUG=False                                    # Nunca True en producción
SECRET_KEY=<clave-secreta-segura>            # Generar con secrets.token_urlsafe(50)
ALLOWED_HOSTS=localhost,tu-dominio.com

# Database (REQUIRED)
DATABASE_URL=postgresql://user:pass@host:port/db

# Security
SECURE_SSL_REDIRECT=True                      # En producción
SESSION_COOKIE_SECURE=True                    # En producción
CSRF_COOKIE_SECURE=True                       # En producción
CSRF_TRUSTED_ORIGINS=https://tu-dominio.com

# CORS
CORS_ALLOWED_ORIGINS=https://tu-dominio.com,https://app.tu-dominio.com

# Logging
DJANGO_LOG_LEVEL=INFO|WARNING|ERROR          # INFO en desarrollo, WARNING en producción

# HTTPS (Producción)
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

---

## 🔒 Seguridad

### ✅ Checklist para Producción

- [ ] `DEBUG=False`
- [ ] `SECURE_SSL_REDIRECT=True`
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] `CSRF_COOKIE_SECURE=True`
- [ ] `.env` NO está en git
- [ ] DATABASE_URL es seguro y privado
- [ ] Certificado SSL instalado
- [ ] ALLOWED_HOSTS actualizado con tu dominio
- [ ] Backup de BD configurado

---

## 📈 Performance

Para aplicaciones con alta carga:

```yaml
# docker-compose.yml
web:
  command: gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 8 --threads 2
```

Ajusta `--workers` según los cores disponibles:
- 2 cores = 4 workers
- 4 cores = 8 workers
- 8 cores = 16 workers

---

## 📚 Referencias

- [Dockerfile oficial](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose docs](https://docs.docker.com/compose/)
- [Django + Docker](https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/gunicorn/)
- [Gunicorn docs](https://gunicorn.org/)
