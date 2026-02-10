# Guía de Instalación - Inventario App

## 📋 Requisitos del Sistema

### Software Necesario

- **Python**: 3.10 o superior
- **PostgreSQL**: 12 o superior
- **pip**: Gestor de paquetes de Python
- **virtualenv**: Para aislamiento de entorno virtual
- **Git**: Control de versiones (opcional)

### Sistemas Operativos Soportados

- Linux (Ubuntu, Debian, CentOS, etc.)
- macOS
- Windows

---

## 🚀 Instalación Paso a Paso

### Paso 1: Clonar el Repositorio

```bash
# Clonar repositorio
git clone https://github.com/Sebas16608/Inventario-app.git

# Entrar al directorio
cd Inventario-app
```

### Paso 2: Crear Entorno Virtual

El entorno virtual aisla las dependencias del proyecto.

**En Linux/macOS:**

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate
```

**En Windows:**

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate
```

#### Verificar Activación

Deberías ver `(venv)` al inicio de la línea del terminal:

```
(venv) usuario@laptop:~/Inventario-app$
```

### Paso 3: Actualizar pip

```bash
pip install --upgrade pip
```

### Paso 4: Instalar Dependencias

```bash
pip install -r requirements.txt
```

#### Dependencias Principales

```
Django==6.0.2                      # Framework web
djangorestframework==3.16.1        # API REST
djangorestframework_simplejwt==5.5.1  # Autenticación JWT
psycopg2-binary==2.9.11           # Adaptador PostgreSQL
python-dotenv==1.2.1              # Variables de entorno
```

### Paso 5: Configurar Base de Datos

#### 5.1 Instalar PostgreSQL

**En Ubuntu/Debian:**

```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

**En macOS (con Homebrew):**

```bash
brew install postgresql
brew services start postgresql
```

**En Windows:**

Descargar e instalar desde [postgresql.org](https://www.postgresql.org/download/windows/)

#### 5.2 Crear Base de Datos

```bash
# Conectar a PostgreSQL
psql -U postgres

# Crear base de datos
CREATE DATABASE inventario_db;

# Crear usuario (reemplaza contraseña)
CREATE USER inventario_user WITH PASSWORD 'tu_contraseña_aqui';

# Dar permisos
ALTER ROLE inventario_user SET client_encoding TO 'utf8';
ALTER ROLE inventario_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE inventario_user SET default_transaction_deferrable TO on;
ALTER ROLE inventario_user SET default_transaction_level TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE inventario_db TO inventario_user;

# Salir
\q
```

#### 5.3 Verificar Conexión

```bash
psql -U inventario_user -d inventario_db -h localhost
```

### Paso 6: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus valores
nano .env  # o usa tu editor favorito
```

#### Contenido de `.env`

```env
# Django Settings
SECRET_KEY=tu-clave-secreta-aqui-minimo-50-caracteres
DEBUG=True

# Database
DATABASE_URL=postgresql://inventario_user:tu_contraseña@localhost:5432/inventario_db

# JWT
JWT_SECRET_KEY=tu-clave-jwt-aqui

# Hosts permitidos (desarrollo)
ALLOWED_HOSTS=localhost,127.0.0.1

# Environment
ENVIRONMENT=development
```

#### Generar SECRET_KEY

```python
# En Python
import secrets
print(secrets.token_urlsafe(50))
```

### Paso 7: Aplicar Migraciones

```bash
# Crear tablas en base de datos
python manage.py migrate

# Verificar resultado
python manage.py showmigrations
```

### Paso 8: Crear Superusuario (Opcional)

```bash
python manage.py createsuperuser
```

Responde las preguntas interactivas:

```
Username: admin
Email: admin@ejemplo.com
Password: ****
Password (again): ****
Superuser created successfully.
```

### Paso 9: Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver
```

#### Salida Esperada

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
February 10, 2024 - 10:30:00
Django version 6.0.2, using settings 'core.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Paso 10: Acceder a Aplicación

- **API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/ (si creaste superusuario)

---

## 🌐 Instalación en Servidor (Producción)

### Requisitos Adicionales

- **Gunicorn**: WSGI application server
- **Nginx**: Web server reverse proxy
- **Supervisor/Systemd**: Gestor de procesos

### Instalación de Gunicorn

```bash
pip install gunicorn
```

### Configurar Systemd (Linux)

Crear `/etc/systemd/system/inventario.service`:

```ini
[Unit]
Description=Inventario App
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/home/usuario/Inventario-app
ExecStart=/home/usuario/Inventario-app/venv/bin/gunicorn core.wsgi:application --bind unix:/tmp/gunicorn.sock
Restart=always

[Install]
WantedBy=multi-user.target
```

Habilitar y ejecutar:

```bash
sudo systemctl daemon-reload
sudo systemctl enable inventario
sudo systemctl start inventario
```

### Configurar Nginx

Crear `/etc/nginx/sites-available/inventario`:

```nginx
upstream inventario {
    server unix:/tmp/gunicorn.sock;
}

server {
    listen 80;
    server_name tu-dominio.com;

    location /static/ {
        alias /home/usuario/Inventario-app/staticfiles/;
    }

    location / {
        proxy_pass http://inventario;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Habilitar:

```bash
sudo ln -s /etc/nginx/sites-available/inventario /etc/nginx/sites-enabled/
sudo systemctl reload nginx
```

---

## 🔍 Verificación de Instalación

### Checklist de Verificación

- [ ] Python 3.10+ instalado: `python --version`
- [ ] PostgreSQL corriendo: `psycopg2-binary` funciona
- [ ] Entorno virtual activado: `(venv)` visible en terminal
- [ ] Dependencias instaladas: `pip list | grep Django`
- [ ] Variables de entorno: Archivo `.env` existe
- [ ] Base de datos: Migraciones aplicadas sin errores
- [ ] Servidor: Inicia sin errores en `http://localhost:8000`

### Prueba de Conectividad

```bash
# En terminal (con venv activado)
python manage.py shell

# En Python shell
from accounts.models import Company
print(Company.objects.all())
# Debería retornar: QuerySet
```

---

## 🚨 Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'django'"

**Solución:**

```bash
# Verificar venv está activado
which python  # debe mostrar ruta en venv/

# Reinstalar dependencias
pip install -r requirements.txt
```

### Problema: "Error connecting to database"

**Solución:**

```bash
# Verificar PostgreSQL está corriendo
sudo systemctl status postgresql

# Verificar DATABASE_URL en .env
cat .env | grep DATABASE_URL

# Probar conexión
psql -U inventario_user -d inventario_db -h localhost
```

### Problema: "Port 8000 is already in use"

**Solución:**

```bash
# Usar puerto diferente
python manage.py runserver 8001

# O matar proceso en puerto 8000
lsof -i :8000
kill -9 <PID>
```

### Problema: "No migrations detected"

**Solución:**

```bash
python manage.py makemigrations
python manage.py migrate
```

### Problema: "Static files not found"

**Solución:**

```bash
python manage.py collectstatic --noinput
```

---

## 📦 Variables de Entorno Completas

Archivo `.env` con todas las opciones:

```env
# ========================================
# Django Configuration
# ========================================
SECRET_KEY=your-secret-key-here-minimum-50-characters
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ========================================
# Database PostgreSQL
# ========================================
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=inventario_db
DATABASE_USER=inventario_user
DATABASE_PASSWORD=tu_contraseña
DATABASE_HOST=localhost
DATABASE_PORT=5432

# O usar DATABASE_URL
DATABASE_URL=postgresql://inventario_user:contraseña@localhost:5432/inventario_db

# ========================================
# Security
# ========================================
JWT_SECRET_KEY=your-jwt-secret-key-here
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# ========================================
# Email Configuration (Opcional)
# ========================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password

# ========================================
# Environment
# ========================================
ENVIRONMENT=development
```

---

## 🎓 Próximos Pasos

1. **Leer documentación:**
   - [README.md](README.md) - Visión general
   - [API.md](API.md) - Documentación de API
   - [MODELOS.md](MODELOS.md) - Estructura de datos

2. **Crear primer usuario:**
   - Acceder a `/admin`
   - Crear empresa
   - Crear usuario/perfil

3. **Probar API:**
   - Usar Postman o cURL
   - Seguir ejemplos en [API.md](API.md)

4. **Desarrollar:**
   - Ver [DESARROLLO.md](DESARROLLO.md) para guía de desarrollo

---

## 📞 Soporte

Si encuentras problemas durante la instalación:

1. Revisar logs: `python manage.py runserver`
2. Verificar variables de entorno: `cat .env`
3. Consultar troubleshooting arriba
4. Crear issue en GitHub

---

**Última actualización**: 10 de febrero de 2026
