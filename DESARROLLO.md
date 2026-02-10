# Guía de Desarrollo - Inventario App

## 🛠️ Configuración del Entorno de Desarrollo

### Requisitos Previos

- Python 3.10+
- PostgreSQL 12+
- pip
- virtualenv

### 1. Configuración Inicial

```bash
# Clonar repositorio
git clone <url-del-repositorio>
cd Inventario-app

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/macOS:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env y configurar:
# - SECRET_KEY: Clave secreta de Django
# - DEBUG: True para desarrollo, False para producción
# - DATABASE_URL: Conexión a PostgreSQL
# - JWT_SECRET_KEY: Clave para firmar tokens JWT
```

### 3. Configurar Base de Datos

```bash
# Aplicar migraciones
python manage.py migrate

# Crear superusuario (para acceso admin)
python manage.py createsuperuser
```

### 4. Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible en `http://localhost:8000`

---

## 📁 Estructura de Directorios y Convenciones

### Estructura General

```
Inventario-app/
├── accounts/                 # Aplicación de autenticación
│   ├── models.py            # Modelos: Company, Profile
│   ├── views.py             # Vistas de autenticación
│   ├── serializers/         # Serializadores
│   ├── services/            # Lógica de negocio
│   ├── migrations/          # Migraciones de BD
│   ├── tests.py             # Tests
│   ├── admin.py             # Configuración admin
│   └── apps.py              # Configuración de app
├── inventario/              # Aplicación principal
│   ├── models/              # Modelos de datos
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── batch.py
│   │   ├── movement.py
│   │   └── __init__.py
│   ├── serializers/         # Serializadores DRF
│   ├── views/               # Vistas de API
│   ├── services/            # Servicios/Lógica
│   ├── migrations/
│   ├── tests.py
│   ├── admin.py
│   └── apps.py
├── core/                    # Configuración central
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── API.py                   # Clase base SuperApiView
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔧 Crear un Nuevo Modelo

### 1. Definir el Modelo

Crear archivo `inventario/models/nuevo_modelo.py`:

```python
from django.db import models
from accounts.models import Company

class NuevoModelo(models.Model):
    # Relaciones
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        related_name="nuevo_modelo"
    )
    
    # Campos
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["id"]
        verbose_name = "Nuevo Modelo"
        verbose_name_plural = "Nuevos Modelos"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "slug"],
                name="unique_modelo_slug_per_company"
            )
        ]
    
    def __str__(self):
        return self.nombre
```

### 2. Importar en `__init__.py`

En `inventario/models/__init__.py`:

```python
from .nuevo_modelo import NuevoModelo

__all__ = [
    'NuevoModelo',
    # otros modelos...
]
```

### 3. Crear Serializador

Crear `inventario/serializers/nuevo_modelo_serializer.py`:

```python
from rest_framework import serializers
from inventario.models.nuevo_modelo import NuevoModelo

class NuevoModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = NuevoModelo
        fields = [
            'id',
            'nombre',
            'descripcion',
            'slug',
            'company',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
```

### 4. Crear Vista

Crear `inventario/views/nuevo_modelo_view.py`:

```python
from API import SuperApiView
from inventario.models.nuevo_modelo import NuevoModelo
from inventario.serializers.nuevo_modelo_serializer import NuevoModeloSerializer

class NuevoModeloView(SuperApiView):
    model = NuevoModelo
    serializer_class = NuevoModeloSerializer
    filter_fields = ['nombre', 'slug']
```

### 5. Registrar URL

En `core/urls.py`:

```python
from inventario.views.nuevo_modelo_view import NuevoModeloView

urlpatterns = [
    # ... otras URLs
    path('nuevo-modelo/', NuevoModeloView.as_view()),
    path('nuevo-modelo/<int:pk>/', NuevoModeloView.as_view()),
]
```

### 6. Registrar en Admin

En `inventario/admin.py`:

```python
from django.contrib import admin
from inventario.models.nuevo_modelo import NuevoModelo

@admin.register(NuevoModelo)
class NuevoModeloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'company', 'created_at')
    search_fields = ('nombre', 'slug')
    list_filter = ('company', 'created_at')
    prepopulated_fields = {'slug': ('nombre',)}
```

### 7. Crear Migración

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🗂️ Estructura de Servicios

Los servicios contienen la lógica de negocio compleja.

Ejemplo: `inventario/services/stock_service.py`

```python
from inventario.models.batch import Batch
from inventario.models.movement import Movement

class StockService:
    @staticmethod
    def get_available_stock(product_id):
        """Calcula el stock disponible actual de un producto"""
        batches = Batch.objects.filter(product_id=product_id)
        total = sum(b.quantity_available for b in batches)
        return total
    
    @staticmethod
    def process_movement(batch, movement_type, quantity):
        """Procesa un movimiento de inventario"""
        if movement_type == "OUT":
            batch.quantity_available -= quantity
        elif movement_type == "IN":
            batch.quantity_available += quantity
        # ... más lógica
        batch.save()
        return batch
```

### Usar en Vistas

```python
from inventario.services.stock_service import StockService

class StockView(APIView):
    def get(self, request, product_id):
        stock = StockService.get_available_stock(product_id)
        return Response({"available_stock": stock})
```

---

## 🧪 Tests Unitarios

### Estructura de Tests

Crear pruebas en `inventario/tests.py` o `inventario/tests/`:

```python
from django.test import TestCase
from inventario.models.product import Product
from inventario.models.category import Category
from accounts.models import Company

class ProductTestCase(TestCase):
    def setUp(self):
        """Configura datos para cada test"""
        self.company = Company.objects.create(name="Test Company")
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category",
            company=self.company
        )
    
    def test_create_product(self):
        """Prueba creación de producto"""
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=self.category,
            supplier="Test Supplier",
            company=self.company
        )
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.company, self.company)
    
    def test_unique_slug_per_company(self):
        """Prueba slug único por empresa"""
        Product.objects.create(
            name="Product 1",
            slug="product",
            category=self.category,
            supplier="Supplier",
            company=self.company
        )
        
        # Intentar crear otro con mismo slug
        with self.assertRaises(Exception):
            Product.objects.create(
                name="Product 2",
                slug="product",
                category=self.category,
                supplier="Supplier",
                company=self.company
            )
```

### Ejecutar Tests

```bash
# Ejecutar todos los tests
python manage.py test

# Ejecutar tests de una app específica
python manage.py test inventario

# Ejecutar test específico
python manage.py test inventario.tests.ProductTestCase.test_create_product

# Con verbosidad
python manage.py test -v 2
```

---

## 📝 Migraciones de Base de Datos

### Crear Migración

Después de modificar modelos:

```bash
python manage.py makemigrations
```

Esto crea archivos en `migrations/` que describen los cambios.

### Aplicar Migraciones

```bash
python manage.py migrate
```

### Ver Estado de Migraciones

```bash
python manage.py showmigrations
```

### Deshacer Migraciones

```bash
# Deshacer última migración de una app
python manage.py migrate inventario 0001

# Deshacer todas
python manage.py migrate inventario zero
```

---

## 🔍 Debugging

### Django Debug Toolbar

Instalar y configurar para desarrollo:

```bash
pip install django-debug-toolbar
```

En `settings.py`:

```python
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```

### Logs

Configurar logs en `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

### Shell de Django

```bash
python manage.py shell

# En el shell:
from inventario.models import Product
Product.objects.all()
```

---

## 🚀 Deployment

### Preparar para Producción

1. **Actualizar `settings.py`:**

```python
DEBUG = False
ALLOWED_HOSTS = ['tudominio.com', 'www.tudominio.com']
SECURE_SSL_REDIRECT = True
```

2. **Recopilar archivos estáticos:**

```bash
python manage.py collectstatic --noinput
```

3. **Ejecutar checks:**

```bash
python manage.py check --deploy
```

### Usar Gunicorn

```bash
pip install gunicorn

gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

### Con Nginx

Configurar Nginx como proxy inverso hacia Gunicorn.

---

## 📋 Checklist de Desarrollo

- [ ] Crear rama feature: `git checkout -b feature/nombre`
- [ ] Implementar funcionalidad en modelo/vista/serializer
- [ ] Escribir tests unitarios
- [ ] Crear migraciones: `makemigrations` y `migrate`
- [ ] Verificar que tests pasen: `python manage.py test`
- [ ] Actualizar documentación
- [ ] Hacer commit descriptivo: `git commit -m "Descripción"`
- [ ] Push a rama: `git push origin feature/nombre`
- [ ] Crear Pull Request para revisión

---

## 🐛 Problemas Comunes

### 1. "ModuleNotFoundError: No module named 'rest_framework'"

```bash
pip install djangorestframework
```

### 2. "Error de conexión a base de datos"

- Verificar PostgreSQL está corriendo
- Verificar DATABASE_URL en .env
- Verificar credenciales

### 3. "Migration conflicts"

```bash
# Mostrar estado
python manage.py showmigrations

# Resolver manualmente si es necesario
python manage.py migrate --fake inventario 0001
```

### 4. "Port 8000 already in use"

```bash
# Usar otro puerto
python manage.py runserver 8001
```

---

## 📚 Recursos Útiles

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [JWT Documentation](https://jwt.io/)

---

## 👥 Estándares de Código

### Nombrado

- **Variables**: snake_case
- **Clases**: PascalCase
- **Constantes**: UPPER_SNAKE_CASE
- **Métodos**: snake_case

### Docstrings

```python
def crear_producto(nombre, categoria):
    """
    Crea un nuevo producto.
    
    Args:
        nombre (str): Nombre del producto
        categoria (int): ID de categoría
    
    Returns:
        Product: Objeto producto creado
    
    Raises:
        ValueError: Si nombre está vacío
    """
    pass
```

### Imports

```python
# Estándar
import os
import sys

# Propios de Django
from django.db import models
from django.contrib.auth.models import User

# De apps locales
from inventario.models import Product
from accounts.models import Company

# De librerías externas
from rest_framework import serializers
```

---

**Última actualización**: 10 de febrero de 2026
