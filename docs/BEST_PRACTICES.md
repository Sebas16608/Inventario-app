# Best Practices - Inventario App

## 🎯 Guía de Mejores Prácticas

Esta guía contiene recomendaciones para desarrollo, seguridad y operación de Inventario App.

---

## 💻 Desarrollo

### 1. Estructura de Código

**✅ BIEN:**
```python
# inventario/services/stock_service.py
class StockService:
    """Servicio para operaciones de inventario."""
    
    @staticmethod
    def get_available_quantity(batch_id: int) -> int:
        """Obtiene cantidad disponible de un lote."""
        batch = Batch.objects.get(id=batch_id)
        return batch.quantity_available
```

**❌ MALO:**
```python
# Lógica en vista directamente
def get_stock(request):
    batch = Batch.objects.get(id=request.GET.get('id'))
    return Response({'qty': batch.qty_avl})
```

### 2. Validación de Datos

**✅ BIEN:**
```python
# En serializer
class MovementSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['movement_type'] == 'OUT':
            if data['batch'].quantity_available < data['quantity']:
                raise ValidationError("Stock insuficiente")
        if data['quantity'] <= 0:
            raise ValidationError("Cantidad debe ser positiva")
        return data
```

**❌ MALO:**
```python
# En vista (sin validación)
def create_movement(request):
    movement = Movement.objects.create(**request.data)
    return Response(MovementSerializer(movement).data)
```

### 3. Queries Eficientes

**✅ BIEN:**
```python
# Use select_related para ForeignKey
products = Product.objects.select_related(
    'category', 
    'company'
).all()

# Use prefetch_related para reverse FK
products = Product.objects.prefetch_related(
    'batches', 
    'batches__movements'
).all()
```

**❌ MALO:**
```python
# N+1 queries problem
for product in Product.objects.all():
    print(product.category.name)  # Query por cada producto!
    for batch in product.batches.all():  # Otra query!
        for movement in batch.movements.all():  # Más queries!
            pass
```

### 4. Manejo de Errores

**✅ BIEN:**
```python
from rest_framework.exceptions import ValidationError
from rest_framework import status

def get_product(self, request, pk):
    try:
        product = Product.objects.get(pk=pk)
        return Response(
            ProductSerializer(product).data,
            status=status.HTTP_200_OK
        )
    except Product.DoesNotExist:
        return Response(
            {'error': 'Producto no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
```

**❌ MALO:**
```python
# Sin manejo de excepciones
def get_product(self, request, pk):
    product = Product.objects.get(pk=pk)  # Puede fallar
    return Response(ProductSerializer(product).data)
```

### 5. Tests

**✅ BIEN:**
```python
from django.test import TestCase

class ProductTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test")
        self.category = Category.objects.create(
            name="Test",
            company=self.company,
            slug="test"
        )
    
    def test_create_product(self):
        product = Product.objects.create(
            name="Test Product",
            slug="test",
            category=self.category,
            company=self.company,
            supplier="Test"
        )
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.category, self.category)
    
    def test_unique_slug_per_company(self):
        Product.objects.create(
            name="P1", slug="p", category=self.category,
            company=self.company, supplier="S"
        )
        with self.assertRaises(Exception):
            Product.objects.create(
                name="P2", slug="p", category=self.category,
                company=self.company, supplier="S"
            )
```

**❌ MALO:**
```python
# Sin tests, difícil de mantener
def create_product(data):
    # Código complejo sin garantías
    return Product.objects.create(**data)
```

### 6. Logging

**✅ BIEN:**
```python
import logging

logger = logging.getLogger(__name__)

def process_movement(batch, movement_type, quantity):
    logger.info(
        f"Processing movement: batch={batch.id}, "
        f"type={movement_type}, qty={quantity}"
    )
    try:
        # Procesar
        logger.info(f"Movement processed successfully")
    except Exception as e:
        logger.error(f"Error processing movement: {str(e)}")
        raise
```

**❌ MALO:**
```python
# Sin logging, difícil debuggear
def process_movement(batch, movement_type, quantity):
    # Código silencioso
    batch.quantity_available -= quantity
    batch.save()
```

---

## 🔐 Seguridad

### 1. Secretos y Credenciales

**✅ BIEN:**
```python
# En settings.py
from os import getenv

SECRET_KEY = getenv('SECRET_KEY')  # De variable de entorno
DEBUG = getenv('DEBUG') == 'True'
DATABASE_URL = getenv('DATABASE_URL')

# En .env (NO commitar)
SECRET_KEY=tu-clave-secreta
DATABASE_URL=postgresql://user:pass@host/db
```

**❌ MALO:**
```python
# Hardcoded - NUNCA hacer esto!
SECRET_KEY = 'abc123-my-secret'
PASSWORD = 'postgres'
API_KEY = 'sk-1234...'
```

### 2. Autenticación

**✅ BIEN:**
```python
# Usar JWT con tiempo de expiración corto
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ALGORITHM': 'HS256',
}

# En requests
headers = {'Authorization': 'Bearer <token>'}
```

**❌ MALO:**
```python
# Token sin expiración, sin HTTPS
headers = {'Authorization': 'Basic username:password'}  # En HTTP!
```

### 3. SQL Injection Prevention

**✅ BIEN:**
```python
# Django ORM previene automáticamente
products = Product.objects.filter(name=user_input)

# O con Q objects
from django.db.models import Q
products = Product.objects.filter(
    Q(name__icontains=search_term) |
    Q(description__icontains=search_term)
)
```

**❌ MALO:**
```python
# ¡NUNCA! SQL directo con input
from django.db import connection
cursor = connection.cursor()
cursor.execute(f"SELECT * FROM products WHERE name = '{user_input}'")
```

### 4. Rate Limiting

**✅ BIEN:**
```bash
# Instalar django-ratelimit
pip install django-ratelimit

# En views
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='100/h', method='GET')
def get_products(request):
    return Response(...)
```

**❌ MALO:**
```python
# Sin límite de requests
def get_products(request):
    return Response(Product.objects.all())
```

### 5. CORS Configuration

**✅ BIEN:**
```python
# En settings.py
CORS_ALLOWED_ORIGINS = [
    "https://tudominio.com",
    "https://www.tudominio.com",
]

# En producción: Solo dominios específicos
CORS_ALLOW_CREDENTIALS = True
```

**❌ MALO:**
```python
# Permite cualquier origen - MUY inseguro
CORS_ALLOWED_ORIGINS = ['*']
```

---

## 📊 Performance

### 1. Database Indexing

**✅ BIEN:**
```python
class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(db_index=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    class Meta:
        indexes = [
            models.Index(fields=['company', 'slug']),
            models.Index(fields=['company', 'name']),
        ]
```

**❌ MALO:**
```python
# Sin índices - queries lentas
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
```

### 2. Pagination

**✅ BIEN:**
```python
# En settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}

# En API requests
GET /api/products/?page=1&page_size=20
```

**❌ MALO:**
```python
# Retorna todos los resultados
def list_products(request):
    return Response(ProductSerializer(
        Product.objects.all(), 
        many=True
    ).data)
```

### 3. Caching

**✅ BIEN:**
```python
from django.core.cache import cache

def get_company_total_stock(company_id):
    cache_key = f'stock_company_{company_id}'
    stock = cache.get(cache_key)
    
    if stock is None:
        stock = calculate_total_stock(company_id)
        cache.set(cache_key, stock, timeout=3600)  # 1 hora
    
    return stock
```

**❌ MALO:**
```python
# Sin caché - recalcula cada vez
def get_company_total_stock(company_id):
    return calculate_total_stock(company_id)  # Lento!
```

### 4. Connection Pooling

**✅ BIEN:**
```python
# En settings.py con pgbouncer
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'pgbouncer-host',  # En lugar de DB directo
        'PORT': 6432,
        'CONN_MAX_AGE': 300,
    }
}
```

**❌ MALO:**
```python
# Sin pooling - conexión por request
DATABASES = {
    'default': {
        'HOST': 'postgresql-host',
        'CONN_MAX_AGE': 0,  # No reutiliza conexiones
    }
}
```

---

## 🚀 Deployment

### 1. Environment Configuration

**✅ BIEN:**
```python
# settings.py
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# En servidor de producción:
# Environment variables seteadas, NO .env file
```

**❌ MALO:**
```python
# Hardcoded para producción
DEBUG = True
ALLOWED_HOSTS = ['*']
```

### 2. Static Files

**✅ BIEN:**
```bash
# Recolectar en CloudFront/S3
python manage.py collectstatic --noinput

# En nginx, servir desde /static/
location /static/ {
    alias /var/www/inventario/staticfiles/;
}
```

**❌ MALO:**
```python
# Servir desde Django en producción - LENTO
STATIC_ROOT = base_dir / 'static'
# y no usar collectstatic
```

### 3. Logging en Producción

**✅ BIEN:**
```python
# Centralizar logs
LOGGING = {
    'version': 1,
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'sentry_sdk.integrations.logging.EventHandler',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/inventario/django.log',
            'maxBytes': 1024 * 1024 * 100,  # 100MB
            'backupCount': 10,
        }
    },
    'root': {
        'handlers': ['sentry', 'file'],
        'level': 'INFO',
    }
}
```

**❌ MALO:**
```python
# Logs en stdout o archivo sin rotación
# Llenan el disco rápidamente
```

### 4. Health Checks

**✅ BIEN:**
```python
# urls.py
path('health/', health_check, name='health-check'),

# views.py
from rest_framework.response import Response

def health_check(request):
    try:
        from django.db import connection
        connection.ensure_connection()
        return Response({'status': 'ok'}, status=200)
    except Exception as e:
        return Response(
            {'status': 'error', 'message': str(e)}, 
            status=503
        )
```

**❌ MALO:**
```python
# Sin health check - load balancer no sabe si está caído
```

### 5. Backups

**✅ BIEN:**
```bash
#!/bin/bash
# backup.sh - Daily backup schedule

BACKUP_DIR="/var/backups/inventario"
DATE=$(date +%Y%m%d_%H%M%S)

# Database backup
pg_dump $DATABASE_URL > "$BACKUP_DIR/db_$DATE.sql"
gzip "$BACKUP_DIR/db_$DATE.sql"

# Encrypt and upload to S3
aws s3 cp "$BACKUP_DIR/db_$DATE.sql.gz" \
  s3://backups-bucket/db-backups/

# Keep only last 30 days
find $BACKUP_DIR -mtime +30 -delete
```

**❌ MALO:**
```python
# Sin backups automáticos
# ¡Un solo disco corrompido = pérdida total!
```

---

## 📈 Monitoring

### 1. Application Metrics

**✅ BIEN:**
```python
# Instalar prometheus_client
from prometheus_client import Counter, Histogram
import time

request_count = Counter(
    'http_requests_total',
    'Total requests',
    ['method', 'endpoint']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'Request duration',
    ['method', 'endpoint']
)
```

**❌ MALO:**
```python
# Sin métricas - no sabes cómo perfomr la app
```

### 2. Error Tracking

**✅ BIEN:**
```python
# Con Sentry
import sentry_sdk

sentry_sdk.init(
    "https://...@sentry.io/123456",
    traces_sample_rate=0.1,
    environment="production"
)

# Los errores se envían automáticamente
```

**❌ MALO:**
```python
# Sin alertas - descubres bugs cuando usuarios se quejan
```

### 3. Database Monitoring

**✅ BIEN:**
```bash
# Monitorear conexiones activas
watch -n 1 "psql -U inventario_user -d inventario_db -c 'SELECT count(*) FROM pg_stat_activity;'"

# Ver queries lentas
SELECT query, mean_exec_time 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;
```

**❌ MALO:**
```bash
# Ignorar los logs, descubrir problemas después
```

---

## 🧹 Code Quality

### 1. Linting

**✅ BIEN:**
```bash
# Instalar herramientas
pip install flake8 pylint black isort

# Ejecutar antes de commit
black .
isort .
flake8
pylint inventario/
```

**❌ MALO:**
```python
# Sin linting - código inconsistente
import os, sys
from datetime import datetime as dt

result=some_func(arg1,arg2,arg3)
```

### 2. Type Hints

**✅ BIEN:**
```python
from typing import Optional, List

def create_batch(
    product_id: int,
    quantity: int,
    price: float
) -> Batch:
    """Crea un nuevo lote."""
    batch = Batch.objects.create(
        product_id=product_id,
        quantity_received=quantity,
        purchase_price=price,
        expiration_date=timezone.now().date()
    )
    return batch

def get_products(
    company_id: int,
    limit: Optional[int] = None
) -> List[Product]:
    """Obtiene productos de una empresa."""
    pass
```

**❌ MALO:**
```python
# Sin type hints - difícil de entender
def create_batch(product_id, quantity, price):
    batch = Batch.objects.create(...)
    return batch
```

### 3. Documentation

**✅ BIEN:**
```python
def calculate_stock_available(batch: Batch) -> int:
    """
    Calcula el stock disponible de un lote.
    
    Suma las entradas, resta las salidas y ajustes,
    considera productos expirados.
    
    Args:
        batch: Objeto Batch a calcular
    
    Returns:
        int: Cantidad disponible actual
    
    Example:
        >>> batch = Batch.objects.get(id=1)
        >>> available = calculate_stock_available(batch)
        >>> print(available)
        87
    """
```

**❌ MALO:**
```python
# Sin documentación
def calc_stock(b):
    return b.qty_available
```

---

## 🤝 Team Practices

### 1. Code Reviews

**✅ BIEN:**
```
1. Crear rama con nombre descriptivo
2. Hacer commit con mensaje claro
3. Hacer PR con descripción detallada
4. Al menos 1 reviewer aprueba
5. CI/CD tests pasan
6. Merge a main
```

**❌ MALO:**
```
1. Push directo a main
2. Commits con "fix" o "update"
3. Sin revisión de código
4. Tests no corren
```

### 2. Documentation

**✅ BIEN:**
```
- Cada feature tiene tests
- Documentación actualizada
- API.md tiene ejemplos
- README.md está al día
- CHANGELOG actualizado
```

**❌ MALO:**
```
- Código sin tests
- Documentación desactualizada
- Solo "vive" en la cabeza del dev
```

### 3. Releases

**✅ BIEN:**
```
- Versionado semántico (MAJOR.MINOR.PATCH)
- CHANGELOG documentado
- Tag en git
- Release notes
- Deploar solo releases
```

**❌ MALO:**
```
- Sem versionado
- Deploy de commits aleatorios
- Sin documentación de cambios
```

---

## ✅ Checklist de Producción

Antes de deployar a producción:

- [ ] DEBUG = True → False
- [ ] Todos los secrets en variables de entorno
- [ ] HTTPS/SSL configurado
- [ ] Database backups automatizados
- [ ] Monitoring activado (Sentry, Prometheus)
- [ ] Logs centralizados
- [ ] Rate limiting configurado
- [ ] CORS apropiadamente configurado
- [ ] Tests pasan (100% cobertura idealmente)
- [ ] Code review completado
- [ ] Documentación actualizada
- [ ] Plan de rollback preparado
- [ ] Health checks implementados
- [ ] Load testing completado
- [ ] Security audit realizado

---

## 💡 Recursos Recomendados

- [Django Best Practices](https://docs.djangoproject.com/en/6.0/topics/db/optimization/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [12 Factor App](https://12factor.net/)
- [Google Cloud Best Practices](https://cloud.google.com/docs/best-practices)

---

**Última actualización**: 10 de febrero de 2026
