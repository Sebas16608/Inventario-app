# Preguntas Frecuentes (FAQ) - Inventario App

## 🎯 Preguntas Generales

### ¿Qué es Inventario App?

Inventario App es un sistema SaaS para gestión de inventarios de múltiples empresas construido con Django REST Framework. Permite a empresas administrar:

- Productos y categorías
- Lotes con seguimiento de vencimiento
- Movimientos de stock (entrada, salida, ajustes)
- Múltiples usuarios con diferentes roles

### ¿Es Inventario App de código abierto?

Este proyecto es privado. El código está disponible solo para colaboradores autorizados.

### ¿Puedo usar esto en producción?

Sí, pero necesitas:
- Configurar correctamente las variables de entorno
- Usar PostgreSQL en lugar de SQLite
- Configurar HTTPS/SSL
- Implementar backups
- Configurar monitoreo

Ver [INSTALACION.md](INSTALACION.md) para detalles.

---

## 💻 Instalación y Configuración

### P: Tengo error "ModuleNotFoundError: No module named 'django'"

**R:** El entorno virtual probablemente no está activado.

```bash
# Verificar que (venv) aparezca en el terminal
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate  # Windows

# Reinstalar dependencias
pip install -r requirements.txt
```

### P: No puedo conectar a la base de datos PostgreSQL

**R:** Verifica los siguientes puntos:

```bash
# 1. PostgreSQL está corriendo
sudo systemctl status postgresql

# 2. Credenciales en .env
cat .env | grep DATABASE_URL

# 3. Base de datos existe
psql -U inventario_user -d inventario_db -h localhost

# 4. Si aún falla, recrea la BD
psql -U postgres
DROP DATABASE inventario_db;
CREATE DATABASE inventario_db;
GRANT ALL PRIVILEGES ON DATABASE inventario_db TO inventario_user;
```

### P: Necesito cambiar el puerto del servidor

**R:** Usa la opción de puerto:

```bash
python manage.py runserver 8001
# o
python manage.py runserver 0.0.0.0:9000
```

### P: ¿Cómo genero SECRET_KEY?

**R:** Usa Python:

```python
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Copiar el resultado a `.env`

### P: Las migraciones fallan con error

**R:** Intenta:

```bash
# Ver estado de migraciones
python manage.py showmigrations

# Resetear migraciones (solo desarrollo)
python manage.py migrate inventario zero
python manage.py migrate accounts zero

# Recrear migraciones
python manage.py makemigrations
python manage.py migrate
```

---

## 🔐 Autenticación y Permisos

### P: ¿Cómo obtengo un token JWT?

**R:** Hacer POST a `/api/token/`:

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario", "password": "contraseña"}'
```

Respuesta:
```json
{
  "access": "eyJ0eXAiOi...",
  "refresh": "eyJ0eXAiOi..."
}
```

### P: Mi token expiró, ¿cómo lo renovo?

**R:** POST a `/api/token/refresh/`:

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "token-anterior"}'
```

### P: ¿Cuánto dura un token JWT?

**R:** Por defecto 1 hora. Configurable en `settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
}
```

### P: ¿Cómo funciona la autenticación multi-empresa?

**R:** Cada usuario tiene un `Profile` vinculado a una empresa específica:

```python
Profile:
  - user → Usuario de Django
  - company → Empresa
  - role → ADMIN, SELLER, WAREHOUSE

# Los datos se filtran automáticamente por empresa
Product.objects.filter(company=user.profile.company)
```

---

## 📦 API y Endpoints

### P: ¿Cómo filtro resultados en GET?

**R:** Usa query parameters:

```bash
GET /api/products/?name=Laptop&supplier=Tech%20Corp
GET /api/products/?name=Laptop
GET /api/batches/?product=1
GET /api/movements/?batch=1&movement_type=OUT
```

Los campos filtrables están definidos en la vista:

```python
class ProductView(SuperApiView):
    filter_fields = ["name", "slug", "supplier"]
```

### P: Recibo error 404 "los datos no fueron encontrados"

**R:** El recurso no existe. Verifica:

```bash
# 1. ID correcto
GET /api/products/999/  # ¿Existe el producto con ID 999?

# 2. Empresa correcta (para filtrado)
GET /api/products/?company=1

# 3. URL correcta (sin typos)
GET /api/products/     # Listar (correcto)
GET /api/product/      # Incorrecto
```

### P: POST retorna 400 Bad Request

**R:** Datos inválidos. Verifica:

```bash
# 1. Content-Type header
-H "Content-Type: application/json"

# 2. JSON válido
# Usa herramienta para validar: https://jsonlint.com/

# 3. Campos requeridos
# Ver en API.md qué campos son obligatorios

# 4. Formato de datos
# Decimales con punto: "10.50" NO "10,50"
# Fechas ISO: "2025-12-31" NO "31/12/2025"
```

### P: Agregué un producto pero no aparece

**R:** Probables causas:

```bash
# 1. Verificar request fue exitoso (201 Created)
curl -i -X POST http://localhost:8000/api/products/ ...

# 2. Producto de empresa diferente
GET /api/products/?company=1

# 3. Error silencioso en BD
python manage.py shell
>>> from inventario.models import Product
>>> Product.objects.all()
```

---

## 📊 Datos e Inventario

### P: ¿Cómo registrar una entrada de producto?

**R:** Crear un `Batch`:

```bash
curl -X POST http://localhost:8000/api/batches/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "quantity_received": 100,
    "quantity_available": 100,
    "purchase_price": "50.00",
    "expiration_date": "2025-12-31",
    "supplier": "Proveedor XYZ"
  }'
```

Opcionalmente, registra un movimiento IN:

```bash
curl -X POST http://localhost:8000/api/movements/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "batch": 1,
    "movement_type": "IN",
    "quantity": 100,
    "note": "Entrada por compra"
  }'
```

### P: ¿Cómo registrar una venta/salida?

**R:** Crear movimiento OUT:

```bash
curl -X POST http://localhost:8000/api/movements/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "batch": 1,
    "movement_type": "OUT",
    "quantity": 10,
    "note": "Venta invoice #123"
  }'
```

**Importante**: Verifica que `quantity_available >= cantidad_vendida`

### P: ¿Qué es un Batch?

**R:** Un lote es un conjunto de unidades del mismo producto recibidas juntas:

```
Producto: Paracetamol 500mg

Batch 1: 1000 unidades, precio $0.10, vence 2025-12-31
Batch 2: 500 unidades, precio $0.09, vence 2026-06-30
Batch 3: 750 unidades, precio $0.08, vence 2026-09-15

Total stock = 2250 unidades (suma de batches)
```

Razones para múltiples batches:
- Precios diferentes
- Fechas de vencimiento diferentes
- Proveedores diferentes

### P: ¿Cómo controlo el stock limitado?

**R:** Verifica antes de vender:

```python
# Obtener stock disponible
batch = Batch.objects.get(id=1)
if batch.quantity_available >= cantidad_vendida:
    # Proceder con venta
else:
    # Mostrar error: "Stock insuficiente"
```

O agregando validación en serializer:

```python
class MovementSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['movement_type'] == 'OUT':
            if data['batch'].quantity_available < data['quantity']:
                raise ValidationError("Stock insuficiente")
        return data
```

### P: Producto con fecha de vencimiento cercana

**R:** Las fechas se almacenan en `Batch.expiration_date`.

Query para alertas:

```python
from django.utils import timezone
from dateutil.relativedelta import relativedelta

# Productos que vencen en próximo mes
fecha_limite = timezone.now() + relativedelta(months=1)
proximos_a_vencer = Batch.objects.filter(
    expiration_date__lte=fecha_limite,
    quantity_available__gt=0
)
```

---

## 🛠️ Desarrollo

### P: Quiero agregar un nuevo modelo

**R:** Ver [DESARROLLO.md - Crear un Nuevo Modelo](DESARROLLO.md#-crear-un-nuevo-modelo)

Pasos resumen:
1. Crear modelo en `models/`
2. Crear serializer en `serializers/`
3. Crear vista en `views/`
4. Registrar URL en `urls.py`
5. Registrar en `admin.py`
6. `makemigrations` y `migrate`

### P: ¿Cómo escribo tests?

**R:** Ver [DESARROLLO.md - Tests Unitarios](DESARROLLO.md#-tests-unitarios)

Estructura básica:

```python
from django.test import TestCase

class MyTestCase(TestCase):
    def setUp(self):
        # Crear datos de prueba
        pass
    
    def test_something(self):
        # Hacer assertion
        self.assertEqual(resultado, esperado)
```

Ejecutar: `python manage.py test`

### P: ¿Dónde pongo la lógica de negocio?

**R:** En `services/`:

```
inventario/
  services/
    stock_service.py       # Lógica de inventario
    report_service.py      # Lógica de reportes
    validation_service.py  # Validaciones complejas
```

Usar en vistas:

```python
from inventario.services.stock_service import StockService

class StockView(APIView):
    def get(self, request):
        stock = StockService.calcular_disponible(producto_id)
        return Response({"stock": stock})
```

### P: ¿Cómo me conecto a shell de Django?

**R:** Usar `python manage.py shell`:

```bash
python manage.py shell

# Luego en Python:
from inventario.models import Product
from accounts.models import Company

company = Company.objects.get(id=1)
products = Product.objects.filter(company=company)
for p in products:
    print(p.name)

# Salir: exit()
```

---

## 🚀 Producción

### P: ¿Es seguro poner esto en producción?

**R:** Sí, pero necesitas:

- [ ] DEBUG = False
- [ ] SECRET_KEY fuerte y único
- [ ] HTTPS/SSL habilitado
- [ ] Base de datos PostgreSQL dedicada
- [ ] Respaldos automáticos
- [ ] Monitoreo activado
- [ ] Variables sensibles en servidor (no en .env)
- [ ] ALLOWED_HOSTS configurado correctamente
- [ ] SECURE_SSL_REDIRECT = True
- [ ] Logs centralizados (Sentry, etc.)

### P: ¿Cómo despiego en producción?

**R:** Ver [INSTALACION.md - Deployment](INSTALACION.md#-deployment)

Resumen:
1. Servidor Linux con Python 3.10+
2. PostgreSQL
3. Gunicorn para servir app
4. Nginx como reverse proxy
5. Systemd para gestionar servicio
6. SSL/TLS certificado

### P: ¿Cómo se hacen respaldos de BD?

**R:** PostgreSQL:

```bash
# Backup completo
pg_dump inventario_db > backup_$(date +%Y%m%d).sql

# Restore
psql inventario_db < backup_20240210.sql

# Backup automático (cron)
# Cada día a las 2 AM:
0 2 * * * pg_dump inventario_db > /backups/inventario_$(date +\%Y\%m\%d).sql
```

### P: ¿Cómo monitoreo la aplicación?

**R:** Opciones:

1. **Sentry** - Rastreo de errores
   ```python
   import sentry_sdk
   sentry_sdk.init("https://...@sentry.io/...")
   ```

2. **New Relic** - Monitoreo APM
3. **Datadog** - Métricas y logs
4. **Prometheus** - Métricas locales

---

## 📚 Documentación

### P: ¿Dónde obtengo documentación del API?

**R:** Ver [API.md](API.md) - Documentación completa de endpoints

Ejemplos:
- Listar productos
- Crear producto
- Actualizar producto
- Deletar producto
- Filtrar resultados

### P: Necesito documentación de los modelos

**R:** Ver [MODELOS.md](MODELOS.md) - Descripción detallada de:
- Company
- Profile
- Category
- Product
- Batch
- Movement

### P: ¿Cómo estructura el código?

**R:** Ver [ARQUITECTURA.md](ARQUITECTURA.md) - Explicación de:
- Capas de la aplicación
- Relaciones entre modelos
- Patrón de diseño
- Multi-tenancy

---

## 🆘 Soporte

### P: Necesito ayuda, ¿a quién contacto?

**R:** Opciones:

1. **Issues de GitHub** - Para bugs y features
2. **Discussions** - Para preguntas generales
3. **Email** - contacto [en desarrollo]

### P: Encontré un bug, ¿cómo reporto?

**R:** Ver [CONTRIBUCIONES.md - Reportar Bugs](CONTRIBUCIONES.md#-reportar-bugs)

Información a incluir:
- Descripción clara
- Pasos para reproducir
- Comportamiento esperado vs actual
- Versiones (Python, Django, OS)
- Logs/mensajes de error

---

## 📞 Contacto

Para preguntas adicionales no listadas aquí:

- Crear issue en GitHub
- Revisar documentación existente
- Contactar con mantenedor

---

**Última actualización**: 10 de febrero de 2026
