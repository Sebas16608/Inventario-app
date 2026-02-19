# Backend - Sistema de Gestión de Inventario

Backend API construida con Django REST Framework para gestión de inventarios multi-empresa.

## 🚀 Características

- **API RESTful** con Django REST Framework
- **Autenticación JWT** con simplejwt (access: 1h, refresh: 7 días)
- **Arquitectura Multi-Tenant** (aislamiento por empresa)
- **Base de datos PostgreSQL** con migraciones automáticas
- **Validación de datos** en serializers
- **Gestión completa de inventario**: categorías, productos, lotes y movimientos
- **CORS habilitado** para frontend

## 🛠️ Requisitos

- Python 3.10+
- PostgreSQL 12+
- pip (gestor de paquetes de Python)

## 📦 Instalación Rápida

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 4. Migraciones
python manage.py migrate

# 5. Ejecutar servidor
python manage.py runserver
```

Servidor en: `http://localhost:8000`

## 🏗️ Estructura

```
backend/
├── accounts/           # Autenticación y usuarios
│   ├── serializers/   # Validadores de entrada
│   ├── views/         # Endpoints auth
│   └── models.py      # User, Company, Profile
├── inventario/         # Gestión de inventario
│   ├── models/        # Category, Product, Batch, Movement
│   ├── serializers/   # API serializers
│   ├── views/         # API endpoints
│   ├── services/      # StockService (lógica de negocio)
│   └── migrations/    # Cambios de BD
├── core/              # Configuración Django
│   ├── settings.py    # Configuración principal
│   ├── urls.py        # Rutas principales
│   └── wsgi.py        # Para producción
├── requirements.txt   # Dependencias
└── manage.py         # Gestor de Django
```

## 🔑 Endpoints Principales

### Autenticación (`/auth/`)
```
POST /auth/register/      - Registrar usuario + empresa
POST /auth/login/         - Login
POST /auth/token/refresh/ - Refrescar token
```

### Categorías (`/api/`)
```
GET    /api/categories/       - Listar
POST   /api/categories/       - Crear
PUT    /api/categories/{id}/  - Actualizar
DELETE /api/categories/{id}/  - Eliminar
```

### Productos (`/api/`)
```
GET    /api/products/         - Listar
POST   /api/products/         - Crear
PUT    /api/products/{id}/    - Actualizar
DELETE /api/products/{id}/    - Eliminar
```

### Lotes (`/api/`)
```
GET    /api/batches/          - Listar
POST   /api/batches/          - Crear
DELETE /api/batches/{id}/     - Eliminar
```

### Movimientos (`/api/`)
```
GET    /api/movements/        - Listar
POST   /api/movements/        - Crear
PATCH  /api/movements/{id}/   - Actualizar
DELETE /api/movements/{id}/   - Eliminar
```

## 🔐 Autenticación JWT

**Flujo:**
1. `POST /auth/register/` → Usuario + empresa
2. `POST /auth/login/` → email + contraseña
3. Respuesta: `access_token` (1h) + `refresh_token` (7d)
4. Incluir en headers: `Authorization: Bearer <token>`

**Refresh:**
```bash
POST /auth/token/refresh/
{
  "refresh": "token-refresh"
}
```

## 🏢 Multi-Tenancy

La arquitectura garantiza aislamiento de datos:
- `BaseCompanyAPIView` - Valida que usuario pertenece a empresa
- Queryset filtering - Filtra automáticamente por empresa
- Serializer context - Pasa empresa al crear/actualizar datos

Ejemplo:
```python
# Solo ve productos de su empresa
GET /api/products/
→ SELECT * FROM products WHERE company_id = request.user.company_id
```

## 💾 Modelos de Datos

### User
```
email, username, password, company, role, profile
```

### Company
```
name, created_at
```

### Category
```
name, slug (único por empresa), company
```

### Product
```
name, slug, category, supplier, cost_price, sale_price, stock, company
```

### Batch
```
product, quantity_received, quantity_available, purchase_price, 
expiration_date, supplier, received_at
```

### Movement
```
batch, product, quantity, movement_type (IN|OUT|ADJUST|EXPIRED), 
reason, created_at, created_by
```

## 📝 Variables de Entorno

```env
SECRET_KEY=django-insecure-...
DEBUG=True
DATABASE_URL=postgresql://user:pass@localhost:5432/inventario_db
JWT_SECRET_KEY=tu-clave-jwt
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## 🔌 Servicios Importantes

### StockService
Maneja la lógica de movimientos de stock:

```python
# Registro de entrada
StockService.registrar_entrada(
    product=product,
    quantity=100,
    purchase_price=10.50,
    expiration_date="2025-12-31",
    supplier="Proveedor X"
)

# Registro de salida
StockService.registrar_salida(
    product=product,
    quantity=50,
    note="Venta cliente"
)
```

## 🧪 Testing

```bash
# Ejecutar tests
python manage.py test

# Con cobertura
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 🚢 Deployment

### Docker
```bash
docker build -t inventario-backend .
docker run -p 8000:8000 --env-file .env inventario-backend
```

### Producción
Ver `docs/RENDER_DEPLOYMENT.md` para deployment en Render.com

## 🔒 Seguridad

✅ Contraseñas hasheadas (PBKDF2)  
✅ CORS restringido a frontend  
✅ Validación de entrada en serializers  
✅ Aislamiento multi-tenant  
✅ JWT con expiración  
✅ Rate limiting recomendado  

## 🐛 Troubleshooting

### Error BD
```bash
# Verificar PostgreSQL
sudo systemctl status postgresql

# Chequear .env
cat .env | grep DATABASE_URL
```

### Migraciones
```bash
# Ver estado
python manage.py showmigrations

# Crear nueva
python manage.py makemigrations

# Aplicar
python manage.py migrate
```

### Puerto ocupado
```bash
python manage.py runserver 8001
```

## 📚 Documentación

- `/docs/API.md` - Documentación API completa
- `/docs/ARQUITECTURA.md` - Diseño arquitectónico
- `/docs/MODELOS.md` - Descripción modelos
- `/docs/JWT_AUTH.md` - Autenticación JWT
- `/docs/BEST_PRACTICES.md` - Buenas prácticas

## 📞 Contacto

Para bugs o sugerencias, crear un issue en el repositorio.│   │   ├── wsgi.py                # WSGI application
│   │   ├── asgi.py                # ASGI application
│   │   ├── urls.py                # URLs raíz
│   │   └── __init__.py
│   │
│   ├── accounts/                   # Gestión de usuarios y autenticación
│   │   ├── models.py              # Modelos de usuario
│   │   ├── views/                 # Vistas (register, login, profile, etc)
│   │   ├── serializers/           # Serializadores DRF
│   │   ├── services/              # Lógica de negocio
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── migrations/
│   │
│   └── inventario/                 # Gestión de inventario
│       ├── models/                 # Modelos (Product, Category, Batch, Movement)
│       ├── views/                  # ViewSets y Vistas
│       ├── serializers/            # Serializadores DRF
│       ├── services/               # Servicios (stock_service, etc)
│       ├── urls.py
│       ├── admin.py
│       └── migrations/
│
├── 📄 CONFIGURACIÓN
│   ├── manage.py                   # Django CLI
│   ├── requirements.txt            # Python dependencies
│   ├── entrypoint.sh               # Script de entrada Docker
│   ├── Dockerfile                  # Dockerfile (opcional)
│   └── __init__.py
│
└── 💾 ALMACENAMIENTO
    ├── logs/                       # Application logs
    ├── media/                      # User uploads
    └── staticfiles/                # Collected statics
```

---

## 🚀 Quick Start

### Requisitos

- Python 3.13+
- pip o poetry
- PostgreSQL 12+ (o SQLite para desarrollo)

### Instalación Local

```bash
# 1. Entrar al directorio backend
cd backend

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno (en la raíz del proyecto)
cd ..
cp .env.example .env
nano .env

# 5. Aplicar migraciones
cd backend
python manage.py migrate

# 6. Crear superusuario (para Django admin)
python manage.py createsuperuser

# 7. Ejecutar servidor
python manage.py runserver

# ✅ Acceder a:
# - API: http://localhost:8000/api/
# - Admin: http://localhost:8000/admin/
# - Docs: http://localhost:8000/api/docs/ (si está configurado)
```

### Instalación con Docker

```bash
# Desde la raíz del proyecto
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Migraciones
docker-compose exec web python backend/manage.py migrate

# Crear superusuario
docker-compose exec web python backend/manage.py createsuperuser
```

---

## 🏛️ Arquitectura

### Estructura de Capas

```
┌─────────────────────────────────────────┐
│         Cliente (Frontend/Mobile)       │
├─────────────────────────────────────────┤
│     API Router (Django URLs)            │
├─────────────────────────────────────────┤
│  ViewSet / APIView (REST Endpoints)     │
├─────────────────────────────────────────┤
│  Serializers (Data Validation)          │
├─────────────────────────────────────────┤
│  Services (Business Logic)              │
├─────────────────────────────────────────┤
│  Models (ORM & Database)                │
├─────────────────────────────────────────┤
│      PostgreSQL Database                │
└─────────────────────────────────────────┘
```

### Apps Principales

#### 1️⃣ **accounts** - Autenticación y Usuarios

```
Modelos:
├── User (Custom user model)
├── UserProfile
└── Company

Endpoints:
├── POST /api/auth/register/      - Registrar nuevo usuario
├── POST /api/auth/login/         - Login (obtener token)
├── POST /api/auth/refresh/       - Refresh token
├── GET  /api/profile/             - Perfil del usuario
└── GET  /api/companies/           - Empresas del usuario
```

#### 2️⃣ **inventario** - Gestión de Inventario

```
Modelos:
├── Category
├── Product
├── Batch
└── Movement

Endpoints:
├── /api/categories/    - CRUD de categorías
├── /api/products/      - CRUD de productos
├── /api/batches/       - CRUD de lotes
├── /api/movements/     - Movimientos de stock
└── /api/stock/         - Vista de stock actual
```

---

## 🔐 Autenticación

### JWT (JSON Web Tokens)

El backend usa **Django REST Simple JWT** para autenticación:

```bash
# 1. Registro
POST /api/auth/register/
{
  "username": "usuario",
  "email": "usuario@example.com",
  "password": "securepassword123"
}

# 2. Login (obtener token)
POST /api/auth/login/
{
  "username": "usuario",
  "password": "securepassword123"
}
# Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

# 3. Usar token en requests
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

📖 Ver [../docs/JWT_AUTH.md](../docs/JWT_AUTH.md) para más detalles.

---

## 📚 Modelos

### User & Company

```python
User
├── username
├── email
├── password (hashed)
├── first_name
├── last_name
├── is_active
└── created_at

Company
├── name
├── industry
├── owner (ForeignKey to User)
└── created_at
```

### Inventario

```python
Category
├── name
├── description
└── company (ForeignKey)

Product
├── name
├── sku (unique)
├── description
├── category (ForeignKey)
├── price
├── cost
├── supplier
├── company (ForeignKey)
└── created_at

Batch
├── batch_number (unique)
├── product (ForeignKey)
├── quantity
├── purchase_price
├── expiration_date
├── manufacturing_date
├── company (ForeignKey)
└── created_at

Movement
├── movement_type (entrada, salida, ajuste, expirado)
├── product (ForeignKey)
├── batch (ForeignKey)
├── quantity
├── reason
├── company (ForeignKey)
└── created_at
```

---

## 🛠️ Comandos Django

### Migraciones

```bash
# Ver migraciones pendientes
python manage.py showmigrations

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Aplicar migraciones de una app específica
python manage.py migrate accounts

# Revertir migraciones
python manage.py migrate accounts 0001_initial  # Vuelve a una migración específica
```

### Management

```bash
# Crear superusuario
python manage.py createsuperuser

# Admin Django
python manage.py runserver
# Ir a http://localhost:8000/admin/

# Shell interactivo
python manage.py shell

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Borrar caché
python manage.py clear_cache
```

### Testing

```bash
# Ejecutar todos los tests
python manage.py test

# Tests de una app específica
python manage.py test accounts
python manage.py test inventario

# Tests verboso
python manage.py test --verbosity=2

# Tests con coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Desarrollo

```bash
# Servidor de desarrollo
python manage.py runserver

# En otro puerto
python manage.py runserver 8001

# Permitir acceso desde la red
python manage.py runserver 0.0.0.0:8000

# Check de configuración
python manage.py check
```

---

## 📝 Desarrollo

### Crear una Nueva App

```bash
# Dentro de backend/
python manage.py startapp nombre_app

# Agregar a INSTALLED_APPS en core/settings.py
INSTALLED_APPS = [
    ...
    'nombre_app',
]

# Crear modelos en nombre_app/models.py
# Crear serializers en nombre_app/serializers.py (o serializers/ folder)
# Crear views en nombre_app/views.py (o views/ folder)
# Crear urls en nombre_app/urls.py
# Agregar a core/urls.py
```

### Crear un Modelo

```python
# backend/nombre_app/models.py
from django.db import models
from django.contrib.auth.models import User

class MiModelo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-creado_en']
        verbose_name = "Mi Modelo"
        verbose_name_plural = "Mis Modelos"
    
    def __str__(self):
        return self.nombre
```

### Crear un Serializer

```python
# backend/nombre_app/serializers/mi_serializer.py
from rest_framework import serializers
from ..models import MiModelo

class MiModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiModelo
        fields = ['id', 'nombre', 'descripcion', 'usuario', 'creado_en']
        read_only_fields = ['id', 'creado_en']
```

### Crear una ViewSet

```python
# backend/nombre_app/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from ..models import MiModelo
from ..serializers.mi_serializer import MiModeloSerializer

class MiModeloViewSet(viewsets.ModelViewSet):
    queryset = MiModelo.objects.all()
    serializer_class = MiModeloSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filtrar por usuario autenticado
        return MiModelo.objects.filter(usuario=self.request.user)
```

### Registrar URLs

```python
# backend/nombre_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MiModeloViewSet

router = DefaultRouter()
router.register(r'mi-modelo', MiModeloViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

---

## 🧪 Testing

### Structure

```
backend/
├── accounts/
│   └── tests.py
├── inventario/
│   └── tests.py
└── core/
    └── tests.py
```

### Escribir Tests

```python
# backend/accounts/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.is_active)
    
    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')
```

### Ejecutar Tests

```bash
# Todos los tests
python manage.py test

# Tests de una app
python manage.py test accounts

# Tests de una clase específica
python manage.py test accounts.tests.UserModelTests

# Con coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 🚀 Deployment

### Render.com

El backend está configurado para deployment automático en Render:

```bash
# Requirements:
1. Procfile en raíz: define web y release commands
2. runtime.txt en raíz: especifica Python 3.13.1
3. requirements.txt: todas las dependencias

# Variables de entorno (en Render):
- DEBUG=False
- SECRET_KEY=<secure-key>
- ALLOWED_HOSTS=yourdomain.com
- DATABASE_URL=<render-postgresql-url>
- SECURE_SSL_REDIRECT=True
# ... y más

# Pasos:
1. git push origin main
2. Conectar repo en render.com
3. Render ejecuta Procfile automáticamente
4. Migraciones se ejecutan en release command
```

Ver [../RENDER_DEPLOYMENT.md](../RENDER_DEPLOYMENT.md) para instrucciones completas.

### Docker

```bash
# Desde raíz del proyecto
docker-compose up -d

# Acceder
curl http://localhost:8000/api/
```

---

## 📊 Configuración de Django

### settings.py

**Ubicación**: `backend/core/settings.py`

**Principales configuraciones**:

```python
# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
    )
}

# Security
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'

# JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# CORS
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
```

---

## 📖 Documentación Adicional

- 🏛️ [../docs/ARQUITECTURA.md](../docs/ARQUITECTURA.md) - Arquitectura completa
- 📋 [../docs/MODELOS.md](../docs/MODELOS.md) - Definición de modelos
- 🔐 [../docs/JWT_AUTH.md](../docs/JWT_AUTH.md) - JWT en detalle
- 🔌 [../docs/API.md](../docs/API.md) - API endpoints
- ✨ [../docs/BEST_PRACTICES.md](../docs/BEST_PRACTICES.md) - Mejores prácticas
- 👨‍💻 [../docs/DESARROLLO.md](../docs/DESARROLLO.md) - Guía de desarrollo
- 🤝 [../docs/CONTRIBUCIONES.md](../docs/CONTRIBUCIONES.md) - Cómo contribuir

---

## 🔧 Troubleshooting

### Error: "No module named 'core'"

```bash
# Asegurar que estás en el directorio correcto
cd backend

# O agregar al PYTHONPATH
export PYTHONPATH=/path/to/backend:$PYTHONPATH
```

### Error: "relation 'auth_user' does not exist"

```bash
python manage.py migrate
```

### Error: PostgreSQL connection

```bash
# Verificar DATABASE_URL
echo $DATABASE_URL

# Crear BD localmente
psql -U postgres -c "CREATE DATABASE inventario_db;"
```

### Error: Static files

```bash
python manage.py collectstatic --noinput --clear
```

---

## 🤝 Contribuir

### Workflow

1. **Fork** el repositorio
2. **Branch** para tu feature: `git checkout -b feature/amazing-feature`
3. **Commit**: `git commit -m 'Add amazing feature'`
4. **Push**: `git push origin feature/amazing-feature`
5. **Pull Request**: Describe tus cambios

### Estándar de Código

- PEP 8 para Python
- Nombres descriptivos
- Docstrings para funciones/clases
- Type hints recomendados
- Tests para nuevas features

### Checklist Antes de PR

- [ ] Tests pasan: `python manage.py test`
- [ ] flake8 check: `flake8 .`
- [ ] Migraciones creadas si cambias modelos
- [ ] Documentación actualizada
- [ ] .env.example actualizado si nuevas variables

Ver [../docs/CONTRIBUCIONES.md](../docs/CONTRIBUCIONES.md) para más detalles.

---

## 📞 Soporte

- 📚 Ver documentación en `docs/`
- 🐛 Reportar bugs en GitHub Issues
- 💬 Discusiones en GitHub Discussions

---

## 📄 Licencia

Privado - Todos los derechos reservados.

---

## 👨‍💻 Autor

**Sebastián** - [GitHub](https://github.com/Sebas16608)

---

**Última actualización**: 17 de febrero de 2026
**Django**: 5.1.5
**Python**: 3.13.1
