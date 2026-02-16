# Inventario-app

**Sistema de Gestión de Inventario Multi-Empresa basado en Django REST Framework**

## 📋 Descripción del Proyecto

Inventario App es una plataforma SaaS para la gestión integral de inventarios que permite a múltiples empresas administrar sus productos, categorías, lotes y movimientos de stock. Está construida con Django 6.0 y Django REST Framework, proporcionando una API RESTful completa y escalable.

### Características Principales

- 🏢 **Multi-empresa**: Cada empresa gestiona su propio inventario de forma independiente
- 📦 **Gestión de Productos**: Organización de productos por categorías
- 📊 **Control de Lotes**: Seguimiento de lotes con fechas de vencimiento y precios
- 🔄 **Movimientos de Inventario**: Registro de entradas, salidas, ajustes y productos expirados
- 👥 **Sistema de Roles**: ADMIN, SELLER, WAREHOUSE
- 🔐 **Autenticación JWT**: Soporte para JWT simplejwt
- 🗄️ **Base de Datos PostgreSQL**: Almacenamiento robusto con PostgreSQL

## 🚀 Quick Start

### Opción 1: Desarrollo Local (sin Docker)

```bash
# Clonar repositorio
git clone https://github.com/Sebas16608/Inventario-app.git
cd Inventario-app

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Aplicar migraciones
python manage.py migrate

# Ejecutar servidor
python manage.py runserver
```

### Opción 2: Docker (Recomendado para Producción)

```bash
# Clonar repositorio
git clone https://github.com/Sebas16608/Inventario-app.git
cd Inventario-app

# Copiar configuración de producción
cp .env.production .env

# Editar variables (SECRET_KEY, ALLOWED_HOSTS, etc)
nano .env

# Construir y ejecutar
docker-compose build
docker-compose up -d

# Ejecutar migraciones
docker-compose exec web python manage.py migrate
```

Para instrucciones detalladas, ver:
- 📖 [docs/INSTALACION.md](docs/INSTALACION.md) - Setup local
- 🐳 [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deploy con Docker

## 📚 Documentación

Toda la documentación está en la carpeta [docs/](docs/):

| Documento | Descripción |
|-----------|-------------|
| [docs/INSTALACION.md](docs/INSTALACION.md) | Guía de instalación y configuración local |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | **Guía de Deploy con Docker y Neon Database** |
| [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md) | Descripción de la arquitectura del sistema |
| [docs/MODELOS.md](docs/MODELOS.md) | Definición de modelos de datos y relaciones |
| [docs/API.md](docs/API.md) | Documentación completa de endpoints de API |
| [docs/DESARROLLO.md](docs/DESARROLLO.md) | Guía para desarrolladores |
| [docs/DOCUMENTACION.md](docs/DOCUMENTACION.md) | Índice completo de toda la documentación |
| [docs/CONTRIBUCIONES.md](docs/CONTRIBUCIONES.md) | Guía de contribución |
| [docs/PREGUNTAS_FRECUENTES.md](docs/PREGUNTAS_FRECUENTES.md) | Preguntas frecuentes y troubleshooting |
| [docs/BEST_PRACTICES.md](docs/BEST_PRACTICES.md) | Mejores prácticas de desarrollo |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Plan de desarrollo futuro |

## 🔌 Endpoints Principales

| Recurso | Métodos | Descripción |
|---------|---------|-------------|
| `/api/products/` | GET, POST | Productos |
| `/api/categories/` | GET, POST | Categorías |
| `/api/batches/` | GET, POST | Lotes de productos |
| `/api/movements/` | GET, POST | Movimientos de inventario |

Ver [docs/API.md](docs/API.md) para documentación completa.

## 🛠️ Tecnologías

### Backend
- **Django 6.0.2** - Framework web principal
- **Django REST Framework 3.16.1** - Marco para APIs REST
- **Django REST Simple JWT 5.5.1** - Autenticación JWT
- **Django CORS Headers 4.3.1** - Configuración CORS

### Base de Datos
- **PostgreSQL 15** - Base de datos principal
- **Neon Database** - Hosting de PostgreSQL en la nube

### Deployment & DevOps
- **Docker** - Containerización
- **Docker Compose** - Orquestación de servicios
- **Gunicorn 21.2.0** - WSGI HTTP Server
- **Nginx** - Reverse Proxy y servidor estático

### Languages & Tools
- **Python 3.10+** - Lenguaje de programación
- **dj-database-url** - Parsing de DATABASE_URL
- **psycopg2-binary** - Driver PostgreSQL

## 🤝 Contribuciones

Para contribuir al proyecto, ver [docs/CONTRIBUCIONES.md](docs/CONTRIBUCIONES.md).

## 📄 Licencia

Este proyecto es privado. Todos los derechos reservados.

## 👨‍💻 Autor

Sebastián - [GitHub](https://github.com/Sebas16608)

---

**Última actualización**: 10 de febrero de 2026
