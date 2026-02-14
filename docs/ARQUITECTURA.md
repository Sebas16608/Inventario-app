# Arquitectura del Sistema - Inventario App

## 🏗️ Visión General

Inventario App está construida usando una arquitectura en capas con Django REST Framework, separando las responsabilidades en diferentes niveles:

```
┌─────────────────────────────────────────┐
│         Cliente (Frontend/Postman)      │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│   Capa de API (API.py - SuperApiView)   │
│  GET, POST, PUT, PATCH, DELETE          │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│  Capa de Vistas (Views)                 │
│  ProductView, CategoryView, etc.        │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│  Capa de Serialización (Serializers)    │
│  Validación y transformación de datos   │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│  Capa de Lógica de Negocio (Services)   │
│  stock_service.py, user-service.py      │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│  Capa de Modelos (Models)               │
│  Product, Category, Batch, Movement     │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│  Capa de Persistencia (Database)        │
│  PostgreSQL                              │
└─────────────────────────────────────────┘
```

## 📦 Estructura de Aplicaciones

### 1. **Accounts** - Gestión de Autenticación y Usuarios

```
accounts/
├── models.py                       # Company, Profile, User (Django built-in)
├── urls.py                         # Rutas de autenticación y usuarios
├── admin.py                        # Configuración admin
├── apps.py                         # Configuración de app
├── tests.py                        # Tests unitarios
├── views/
│   ├── __init__.py
│   ├── login_view.py              # Vista de login
│   ├── register_view.py           # Vista de registro
│   ├── user_view.py               # Vista CRUD de usuarios
│   ├── profile_view.py            # Vista CRUD de perfiles
│   └── company_view.py            # Vista CRUD de empresas
├── serializers/
│   ├── __init__.py
│   ├── login_serializer.py
│   ├── register_serializer.py
│   ├── user_serializer.py
│   ├── profile_serializer.py
│   └── company_serializer.py
├── services/
│   ├── __init__.py
│   └── user_service.py            # Lógica de usuarios
├── migrations/
└── __init__.py
```

#### Modelos Principales:

- **Company**: Empresa/Organización
  - Propietario de todos los datos de inventario
  - Un usuario puede pertenecer a múltiples empresas
  
- **Profile**: Perfil de usuario
  - Relación OneToOne con User de Django
  - Define rol del usuario (ADMIN, SELLER, WAREHOUSE)
  - Vinculado a una empresa específica

### 2. **Inventario** - Gestión de Productos e Inventario

```
inventario/
├── models/
│   ├── category.py     # Modelo Category
│   ├── product.py      # Modelo Product
│   ├── batch.py        # Modelo Batch
│   ├── movement.py     # Modelo Movement
│   └── __init__.py
├── serializers/
│   ├── category_serializer.py
│   ├── product_serializer.py
│   ├── batch_serializer.py
│   ├── movement_serializer.py
│   └── __init__.py
├── views/
│   ├── category_view.py
│   ├── product_view.py
│   ├── stock_view.py
│   └── __init__.py
├── services/
│   ├── stock_service.py # Lógica de inventario
│   └── __init__.py
├── admin.py            # Configuración admin
├── apps.py             # Configuración de app
├── tests.py            # Tests unitarios
├── migrations/
└── __init__.py
```

#### Flujo de Datos:

```
Request POST /api/products/
    ↓
ProductView (hereda de SuperApiView)
    ↓
ProductSerializer.validate()
    ↓
Product.save()
    ↓
Response 201 Created
```

### 3. **Core** - Configuración Central

```
core/
├── settings.py         # Configuración de Django
├── urls.py             # Rutas principales
├── wsgi.py             # Punto de entrada WSGI
├── asgi.py             # Punto de entrada ASGI
└── __init__.py
```

### 4. **API.py** - Clase Base para Vistas

La clase `SuperApiView` implementa CRUD genérico reutilizable:

```python
class SuperApiView(APIView):
    model = None           # Modelo a usar
    serializer_class = None # Serializador a usar
    filter_fields = []     # Campos para filtrado

    # Métodos disponibles:
    - get(request, pk=None)      # GET / GET by ID
    - post(request)              # POST (crear)
    - put(request, pk)           # PUT (actualizar completo)
    - patch(request, pk)         # PATCH (actualizar parcial)
    - delete(request, pk)        # DELETE
```

## 🔄 Relaciones entre Modelos

```
┌─────────────┐
│   Company   │
└──────┬──────┘
       │
       │ (1:N)
       │
       ├─────────────────┬──────────────────┐
       │                 │                  │
       ▼                 ▼                  ▼
   ┌────────┐    ┌─────────┐      ┌─────────┐
   │Category │    │ Product │      │ Profile │
   │         │    │         │      │         │
   │- name   │    │- name   │      │- role   │
   │- slug   │    │- slug   │      │- user   │
   └────────┘    └────┬────┘      └─────────┘
       ▲              │
       │ (1:N)        │ (1:N)
       │              │
       │              ▼
       │          ┌────────┐
       └──────────│ Batch  │
                  │        │
                  │- qty   │
                  │- price │
                  │- expiry│
                  └───┬────┘
                      │ (1:N)
                      │
                      ▼
                  ┌─────────────┐
                  │  Movement   │
                  │             │
                  │- type       │
                  │- quantity   │
                  │- created_at │
                  └─────────────┘
```

### Explicación de Relaciones:

1. **Company → Category** (1:N)
   - Una empresa tiene múltiples categorías
   - Las categorías no compartidas entre empresas

2. **Company → Product** (indirecto a través de Category)
   - Una empresa tiene múltiples productos

3. **Category → Product** (1:N)
   - Una categoría contiene múltiples productos

4. **Product → Batch** (1:N)
   - Un producto puede tener múltiples lotes
   - Diferentes lotes = diferentes fechas de vencimiento o precios

5. **Batch → Movement** (1:N)
   - Un lote registra múltiples movimientos
   - Entradas, salidas, ajustes, etc.

6. **Company → Profile** (1:N)
   - Una empresa tiene múltiples usuarios (con sus perfiles)

## 🔐 Multi-Tenancy (Multi-Empresa)

El sistema está diseñado para soportar múltiples empresas de forma segura:

### Aislamiento de Datos:

```python
# Los datos siempre se filtran por empresa
Product.objects.filter(company=current_user_company)
Batch.objects.filter(product__company=current_user_company)
Category.objects.filter(company=current_user_company)
```

### Restricciones Únicas:

- `Unique(company, slug)` en Category y Product
- Evita conflictos de nombres entre empresas

## 📊 Operaciones Principales

### 1. Gestión de Productos

```
1. Crear Categoría
   POST /api/categories/ → Category creada

2. Crear Producto
   POST /api/products/ → Product creado
   (vinculado a Category y Company)

3. Listar Productos
   GET /api/products/?company=1 → Lista filtrada
```

### 2. Gestión de Inventario

```
1. Recibir Lote
   POST /api/batches/ → Batch creado
   (product, quantity_received, purchase_price, expiration_date)

2. Registrar Movimiento OUT
   POST /api/movements/ → Movement (OUT) creado
   (batch, quantity, movement_type='OUT')
   → stock_service actualiza quantity_available

3. Registrar Movimiento IN
   POST /api/movements/ → Movement (IN) creado
   → stock_service actualiza quantity_available
```

### 3. Control de Stock

```
Quantity Available = Quantity Received - Total Salidas
                   + Ajustes - Expirados
```

## 🔌 Flujo de Autenticación

```
1. Usuario inicia sesión
2. Recibe token JWT
3. Envía token en header Authorization
4. Servidor valida token y obtiene empresa del usuario
5. Filtra datos por empresa
6. Retorna respuesta
```

## 🛠️ Patrones de Diseño

### 1. **Patrón Repository** (via Django ORM)
- Los modelos actúan como repositorio
- QuerySet proporciona abstracción de datos

### 2. **Patrón Service**
- La lógica de negocio está en `services/`
- Ejemplo: `stock_service.py` maneja cálculos de stock

### 3. **Patrón Serializer**
- Validación de entrada de datos
- Serialización de respuestas

### 4. **Patrón Strategy** (Views)
- `SuperApiView` proporciona implementación estándar de CRUD
- Vistas específicas heredan y customizam si es necesario

## 🚀 Escalabilidad

### Consideraciones para Escalar:

1. **Caché**: Agregar Redis para caché de consultas frecuentes
2. **Búsqueda**: Elasticsearch para búsquedas avanzadas
3. **Celery**: Para tareas asincrónicas (reportes, procesamiento)
4. **Replicación**: Configurar replicación de base de datos
5. **CDN**: Para archivos estáticos y media
6. **Load Balancer**: Nginx o HAProxy para distribuir carga

## 📈 Consideraciones de Rendimiento

### Optimizaciones Implementadas:

```python
# select_related en ForeignKey
Product.objects.select_related('category', 'company')

# prefetch_related en Reverse FK
company.products.prefetch_related('batches')
```

### Índices Recomendados:

- `company_id` en Category, Product, Profile
- `batch_id` en Movement
- `slug` junto con `company_id` (composite index)

---

**Última actualización**: 10 de febrero de 2026
