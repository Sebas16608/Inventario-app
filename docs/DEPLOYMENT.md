# Inventario App - Estructura del Proyecto

Este proyecto está reorganizado con una estructura clara de frontend y backend.

## Estructura de Carpetas

```
Inventario-app/
├── backend/                      # Aplicación Django
│   ├── core/                     # Configuración principal de Django
│   ├── accounts/                 # App de autenticación
│   ├── inventario/               # App principal de inventario
│   ├── manage.py                 # Script de gestión Django
│   ├── API.py                    # Clases base de API
│   ├── requirements.txt          # Dependencias Python
│   ├── Dockerfile                # Configuración Docker
│   ├── entrypoint.sh             # Script de inicio del contenedor
│   ├── Procfile                  # Configuración para Render/Heroku
│   ├── runtime.txt               # Versión de Python para Render
│   ├── build.sh                  # Script de build para Render
│   ├── logs/                     # Archivos de log
│   ├── staticfiles/              # Archivos estáticos (generado)
│   └── media/                    # Archivos subidos por usuarios
│
├── frontend/                     # Aplicación Frontend (vacío por ahora)
│
├── docs/                         # Documentación del proyecto
├── docker-compose.yml            # Orquestación de contenedores
├── render.yaml                   # Configuración para Render
├── nginx.conf                    # Configuración Nginx (producción)
├── manage.py                     # Wrapper para ejecutar Django desde raíz
├── .env                          # Variables de entorno (no commitear)
├── .env.example                  # Ejemplo de variables de entorno
└── README.md                     # Este archivo
```

## Configuración Local

### Requisitos
- Python 3.13+
- PostgreSQL (opcional, SQLite funciona para desarrollo)
- Docker y Docker Compose (opcional)

### Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd Inventario-app
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r backend/requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones locales
```

5. **Ejecutar migraciones**
```bash
python manage.py migrate
```

6. **Iniciar servidor de desarrollo**
```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## Docker Local

### Construir imagen
```bash
docker build -f backend/Dockerfile -t inventario-app .
```

### Ejecutar con Docker Compose
```bash
docker-compose up -d
```

Para ejecutar con Nginx (producción):
```bash
docker-compose --profile production up -d
```

## Deployment en Render

### Requisitos
- Cuenta en [Render.com](https://render.com)
- Repositorio en GitHub

### Pasos de Deployment

1. **Conectar repositorio a Render**
   - Ir a Render Dashboard → New Web Service
   - Seleccionar el repositorio de GitHub
   - Seleccionar rama: `main`

2. **Configurar el servicio**
   - Name: `inventario-backend`
   - Runtime: `Python 3.13`
   - Build Command: 
     ```bash
     cd backend && pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
   - Start Command:
     ```bash
     cd backend && gunicorn core.wsgi:application --bind 0.0.0.0:8000
     ```

3. **Agregar variables de entorno**
   - `DEBUG`: `false`
   - `SECRET_KEY`: (generar una segura)
   - `ALLOWED_HOSTS`: `inventario-backend.onrender.com,localhost`
   - `DATABASE_URL`: (proporcionada por Render)
   - `SECURE_SSL_REDIRECT`: `true`
   - `SESSION_COOKIE_SECURE`: `true`
   - `CSRF_COOKIE_SECURE`: `true`
   - `CSRF_TRUSTED_ORIGINS`: `https://inventario-backend.onrender.com`
   - `CORS_ALLOWED_ORIGINS`: `https://inventario-backend.onrender.com`

4. **Crear base de datos PostgreSQL en Render**
   - Render Dashboard → New PostgreSQL
   - Copiar la `CONNECTION_STRING` 
   - Usar como `DATABASE_URL` en el servicio web

5. **Deploy**
   - Click en "Deploy" en Render Dashboard
   - El deployment se completará automáticamente

### Variables de Entorno Importantes

| Variable | Desarrollo | Producción |
|----------|-----------|-----------|
| `DEBUG` | `True` | `False` |
| `SECURE_SSL_REDIRECT` | `False` | `True` |
| `SESSION_COOKIE_SECURE` | `False` | `True` |
| `CSRF_COOKIE_SECURE` | `False` | `True` |

## Estructura de URLs

- **API REST**: `/api/*`
- **Admin**: `/admin/` (solo con autenticación)
- **Autenticación**: `/api/auth/*`

## Troubleshooting

### Error: "DATABASE_URL not set"
```bash
# Asegúrate de configurar DATABASE_URL en .env
export DATABASE_URL="postgresql://user:password@localhost:5432/inventario_db"
```

### Error: "Secret Key not found"
```bash
# Generar una nueva SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Archivos estáticos no se sirven
```bash
python manage.py collectstatic --noinput --clear
```

## API Documentation

Ver `/docs` para documentación de API (si está configurada).

## Contribuir

Ver `docs/CONTRIBUCIONES.md` para guías de contribución.

## Licencia

[Especificar licencia]

## Soporte

Para reportar issues, usa GitHub Issues.
