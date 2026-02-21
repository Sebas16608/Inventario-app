# INVORAX

> **Sistema de Gestión de Inventario Multi-Empresa**
> 
> Minimalista. Rápido. Confiable. Diseñado para el control.
> 
> ✅ Backend listo para producción • 🚀 Deployment en Render • 🐳 Docker containerizado

---

## 📋 Descripción del Proyecto

INVORAX es una plataforma SaaS para la gestión integral de inventarios que permite a múltiples empresas administrar sus productos, categorías, lotes y movimientos de stock. Está construida con **Django 5.1** y **Django REST Framework** en el backend, y **Next.js 14** con TypeScript en el frontend.

### ✨ Características Principales

- 🏢 **Multi-empresa**: Cada empresa gestiona su propio inventario de forma independiente
- 📦 **Gestión de Productos**: Organización de productos por categorías y proveedores
- 📊 **Control de Lotes**: Seguimiento de lotes con fechas de vencimiento y precios
- 🔄 **Movimientos de Inventario**: Registro de entradas, salidas, ajustes y productos expirados
- 👥 **Sistema de Roles**: ADMIN, SELLER, WAREHOUSE con permisos granulares
- 🔐 **Autenticación JWT**: Seguridad con tokens JWT simplejwt
- 🗄️ **PostgreSQL**: Base de datos robusta y escalable
- 🐳 **Docker Ready**: Containerización completa para desarrollo y producción
- ☁️ **Render.com Ready**: Configuración lista para deployment en Render

---

## 🚀 Inicio Rápido

### 📖 Documentación Rápida

| Documento | Propósito |
|-----------|-----------|
| **[QUICKSTART.md](QUICKSTART.md)** | 👈 **COMIENZA AQUÍ** - Instrucciones rápidas |
| **[FRONTEND_SETUP.md](FRONTEND_SETUP.md)** | 🎨 Guía de setup del frontend Next.js |
| **[FRONTEND_SUMMARY.md](FRONTEND_SUMMARY.md)** | 📊 Resumen de lo que incluye el frontend |
| **[FRONTEND_CRUD_GUIDE.md](FRONTEND_CRUD_GUIDE.md)** | 🔧 Cómo completar operaciones CRUD |
| [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) | Deployment en Render.com |
| [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) | Checklist pre-deployment |
| [backend/README.md](backend/README.md) | Guía del backend Django |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Estructura del proyecto |
| [backend/README.md](backend/README.md) | Guía del backend Django |

### 🐳 Opción A: Docker (Recomendado)

```bash
# Clonar y preparar
git clone https://github.com/Sebas16608/Inventario-app.git
cd Inventario-app

# Configurar ambiente
cp .env.example .env
nano .env  # Editar variables

# Iniciar con Docker
docker-compose up -d

# Acceder a la app
open http://localhost:8000
```

### 🐍 Opción B: Desarrollo Local

```bash
# Crear entorno virtual
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar ambiente
cp ../.env.example ../.env
nano ../.env

# Migraciones
python manage.py migrate

# Servidor
python manage.py runserver
```

### ☁️ Opción C: Render.com (Producción)

```bash
# Ver RENDER_DEPLOYMENT.md para pasos completos
# Resumen:
# 1. git push origin main
# 2. Conectar repo en render.com
# 3. Render ejecuta automáticamente Procfile
```

---

## 📊 Estructura del Proyecto

```
INVORAX/
│
├── 🔙 backend/                    # Django application (PRODUCTION READY)
│   ├── core/                      # Settings, WSGI, URLs
│   ├── accounts/                  # Autenticación y usuarios
│   ├── inventario/                # Gestión de inventario
│   ├── manage.py
│   ├── requirements.txt
│   ├── README.md                  # Guía del backend ⭐
│   └── entrypoint.sh
│
├── 🎨 frontend/                   # Next.js 14 + TypeScript (✅ READY!)
│   ├── app/                       # Páginas
│   ├── components/                # Componentes reutilizables
│   ├── lib/                       # Cliente API y hooks
│   ├── types/                     # TypeScript types
│   ├── package.json
│   ├── README.md                  # Documentación frontend ⭐
│   └── quickstart.sh              # Setup automático
│
├── 🐳 DOCKER
│   ├── Dockerfile                 # Imagen principal
│   ├── docker-compose.yml         # Desarrollo local
│   ├── .dockerignore
│   └── build.sh
│
├── 🌐 DEPLOYMENT
│   ├── Procfile                   # Render deployment
│   ├── render.yaml                # Configuración Render
│   ├── runtime.txt                # Python version
│   └── RENDER_DEPLOYMENT.md       # Guía completa
│
├── 📖 DOCUMENTACIÓN
│   ├── QUICKSTART.md              # COMIENZA AQUÍ
│   ├── PROJECT_STRUCTURE.md
│   ├── DEPLOYMENT_CHECKLIST.md
│   ├── .env.example
│   └── docs/                      # Documentación adicional
│
└── 🔧 SCRIPTS
    ├── verify-setup.sh            # Verificar estructura
    └── build.sh                   # Build script
```

---

## 🔌 API Endpoints

| Recurso | Métodos | Documentación |
|---------|---------|---------------|
| `/api/products/` | GET, POST, PUT, DELETE | Productos |
| `/api/categories/` | GET, POST, PUT, DELETE | Categorías |
| `/api/batches/` | GET, POST, PUT, DELETE | Lotes |
| `/api/movements/` | GET, POST | Movimientos |
| `/api/auth/` | POST | Autenticación JWT |
| `/admin/` | - | Django Admin |

Ver [docs/API.md](docs/API.md) para documentación completa.

---

## 🛠️ Tecnologías

### Backend
- **Django 5.1.5** - Framework web principal
- **Django REST Framework 3.14** - APIs REST
- **Django REST Simple JWT** - Autenticación JWT
- **Django CORS Headers** - CORS configurado
- **psycopg2-binary** - Driver PostgreSQL

### Frontend
- **Next.js 14** - Framework React
- **TypeScript** - Tipado estático
- **TailwindCSS** - Estilos
- **React Query** - Gestión de estado

### DevOps & Deployment
- **Python 3.13.1** - Versión Python
- **PostgreSQL 15+** - Base de datos
- **Docker** - Containerización
- **Gunicorn** - WSGI server
- **Nginx** - Reverse proxy
- **Render.com** - Cloud deployment

---

## 📚 Documentación Completa

### Setup & Deployment
- 📖 [QUICKSTART.md](QUICKSTART.md) - Inicio rápido
- 🌐 [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Deploy en Render
- ✅ [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Checklist pre-deploy
- 🏗️ [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Estructura detallada

### Backend Documentation
- 🔙 [backend/README.md](backend/README.md) - Guía del backend
- 🏛️ [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md) - Arquitectura del sistema
- 📋 [docs/MODELOS.md](docs/MODELOS.md) - Modelos de datos
- 🔐 [docs/JWT_AUTH.md](docs/JWT_AUTH.md) - Autenticación JWT
- 🔌 [docs/API.md](docs/API.md) - API endpoints
- 📖 [docs/INSTALACION.md](docs/INSTALACION.md) - Instalación detallada

### Development
- 👨‍💻 [docs/DESARROLLO.md](docs/DESARROLLO.md) - Guía de desarrollo
- ✨ [docs/BEST_PRACTICES.md](docs/BEST_PRACTICES.md) - Mejores prácticas
- 🤝 [docs/CONTRIBUCIONES.md](docs/CONTRIBUCIONES.md) - Guía de contribución
- ❓ [docs/PREGUNTAS_FRECUENTES.md](docs/PREGUNTAS_FRECUENTES.md) - FAQ
- 🗺️ [docs/ROADMAP.md](docs/ROADMAP.md) - Roadmap del proyecto

---

## ⚡ Comandos Útiles

### Docker

```bash
# Ver estado
docker-compose ps

# Logs en vivo
docker-compose logs -f web

# Ejecutar migraciones
docker-compose exec web python backend/manage.py migrate

# Crear superusuario
docker-compose exec web python backend/manage.py createsuperuser

# Shell Django
docker-compose exec web python backend/manage.py shell

# Detener servicios
docker-compose down
```

### Django (Local)

```bash
cd backend

# Migraciones
python manage.py migrate
python manage.py makemigrations

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Ejecutar tests
python manage.py test

# Shell interactivo
python manage.py shell
```

### Frontend (Next.js)

```bash
cd frontend

# Instalar dependencias
npm install

# Desarrollo
npm run dev

# Build producción
npm run build

# Lint
npm run lint
```

---

## 🔐 Seguridad

### ✅ Configurado

- ✅ JWT Authentication (Simple JWT)
- ✅ CORS configurado
- ✅ CSRF protection
- ✅ SQL Injection prevention
- ✅ XSS protection
- ✅ HTTPS ready (SECURE_SSL_REDIRECT)
- ✅ HSTS headers
- ✅ Secure cookies

### 🔒 En Producción

- DEBUG = False
- SECURE_SSL_REDIRECT = True
- SESSION_COOKIE_SECURE = True
- CSRF_COOKIE_SECURE = True

Ver [docs/BEST_PRACTICES.md](docs/BEST_PRACTICES.md) para más detalles.

---

## 🐛 Troubleshooting

### Error: "No module named 'core'"
```bash
# PYTHONPATH debe ser configurado
export PYTHONPATH=/path/to/backend:$PYTHONPATH
```

### Error: PostgreSQL connection
```bash
# Verificar DATABASE_URL
echo $DATABASE_URL

# Local - crear DB
psql -U postgres -c "CREATE DATABASE inventario_db;"
```

### Docker error
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

Ver [docs/PREGUNTAS_FRECUENTES.md](docs/PREGUNTAS_FRECUENTES.md) para más soluciones.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

Ver [docs/CONTRIBUCIONES.md](docs/CONTRIBUCIONES.md) para más detalles.

---

## 📄 Licencia

Privado - Todos los derechos reservados.

---

## 👨‍💻 Autor

**Sebastián** - [GitHub](https://github.com/Sebas16608)

---

## 🚀 Status

```
✅ Backend production-ready
✅ Frontend production-ready
✅ Docker configurado
✅ Render.com ready
```

**Última actualización**: 21 de febrero de 2026
