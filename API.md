# Documentación de API - Inventario App

## 🔌 Base URL

```
http://localhost:8000/api
```

## 🔐 Autenticación

La API utiliza **JWT (JSON Web Tokens)** para autenticación.

### Obtener Token

```bash
POST /api/token/
Content-Type: application/json

{
  "username": "usuario",
  "password": "contraseña"
}
```

**Respuesta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Usar Token en Requests

Incluir token en header `Authorization`:

```bash
Authorization: Bearer <access_token>
```

### Renovar Token

```bash
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## 📋 Respuestas Estándar

### Respuesta Exitosa

```json
{
  "id": 1,
  "name": "Producto",
  "slug": "producto",
  ...
}
```

**Status Code**: `200 OK`

### Respuesta de Creación

```json
{
  "id": 1,
  "name": "Producto",
  ...
}
```

**Status Code**: `201 Created`

### Error 404 No Encontrado

```json
{
  "error": "los datos no fueron encontrados"
}
```

**Status Code**: `404 Not Found`

### Error 400 Validación

```json
{
  "field_name": ["Error message"],
  "another_field": ["Another error message"]
}
```

**Status Code**: `400 Bad Request`

### Eliminación Exitosa

**Status Code**: `204 No Content` (sin body)

---

## 📦 Endpoints de Productos

### Listar Productos

```http
GET /api/products/
```

**Query Parameters:**
- `name` (string) - Filtrar por nombre
- `slug` (string) - Filtrar por slug
- `supplier` (string) - Filtrar por proveedor

**Ejemplo:**
```bash
GET /api/products/?supplier=Tech%20Supplier
Authorization: Bearer <token>
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "slug": "laptop",
    "category": 1,
    "presentation": "Unidad",
    "supplier": "Tech Supplier",
    "company": 1,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### Obtener Producto por ID

```http
GET /api/products/{id}/
```

**Parámetros de Ruta:**
- `id` (integer) - ID del producto

**Ejemplo:**
```bash
GET /api/products/1/
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "id": 1,
  "name": "Laptop",
  "slug": "laptop",
  "category": 1,
  "presentation": "Unidad",
  "supplier": "Tech Supplier",
  "company": 1,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

### Crear Producto

```http
POST /api/products/
Content-Type: application/json
```

**Body Requerido:**
```json
{
  "name": "Laptop",
  "slug": "laptop",
  "category": 1,
  "presentation": "Unidad",
  "supplier": "Tech Supplier",
  "company": 1
}
```

**Campos:**
| Campo | Tipo | Requerido | Descripción |
|-------|------|----------|-------------|
| `name` | string | ✓ | Nombre del producto |
| `slug` | string | ✓ | URL-friendly identifier |
| `category` | integer | ✓ | ID de categoría |
| `presentation` | string | | Formato de presentación |
| `supplier` | string | ✓ | Nombre del proveedor |
| `company` | integer | ✓ | ID de empresa |

**Ejemplo:**
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "Laptop",
    "slug": "laptop",
    "category": 1,
    "presentation": "Unidad",
    "supplier": "Tech Supplier",
    "company": 1
  }'
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "name": "Laptop",
  "slug": "laptop",
  "category": 1,
  "presentation": "Unidad",
  "supplier": "Tech Supplier",
  "company": 1,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

### Actualizar Producto (PUT)

```http
PUT /api/products/{id}/
Content-Type: application/json
```

**Body Requerido:** (todos los campos)
```json
{
  "name": "Laptop Pro",
  "slug": "laptop-pro",
  "category": 1,
  "presentation": "Unidad",
  "supplier": "Tech Supplier",
  "company": 1
}
```

**Ejemplo:**
```bash
curl -X PUT http://localhost:8000/api/products/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "Laptop Pro",
    "slug": "laptop-pro",
    "category": 1,
    "presentation": "Unidad",
    "supplier": "Tech Supplier",
    "company": 1
  }'
```

---

### Actualizar Parcialmente Producto (PATCH)

```http
PATCH /api/products/{id}/
Content-Type: application/json
```

**Body Opcional:** (solo campos a actualizar)
```json
{
  "name": "Laptop Pro",
  "supplier": "New Supplier"
}
```

**Ejemplo:**
```bash
curl -X PATCH http://localhost:8000/api/products/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "Laptop Pro"
  }'
```

---

### Eliminar Producto

```http
DELETE /api/products/{id}/
```

**Ejemplo:**
```bash
curl -X DELETE http://localhost:8000/api/products/1/ \
  -H "Authorization: Bearer <token>"
```

**Respuesta:** 204 No Content

---

## 📂 Endpoints de Categorías

### Listar Categorías

```http
GET /api/categories/
```

**Query Parameters:**
- `name` (string) - Filtrar por nombre
- `slug` (string) - Filtrar por slug

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "Electrónica",
    "description": "Productos electrónicos",
    "slug": "electronica",
    "company": 1,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### Obtener Categoría por ID

```http
GET /api/categories/{id}/
```

---

### Crear Categoría

```http
POST /api/categories/
Content-Type: application/json
```

**Body:**
```json
{
  "name": "Electrónica",
  "description": "Productos electrónicos",
  "slug": "electronica",
  "company": 1
}
```

---

### Actualizar Categoría (PUT/PATCH)

```http
PUT /api/categories/{id}/
PATCH /api/categories/{id}/
```

---

### Eliminar Categoría

```http
DELETE /api/categories/{id}/
```

---

## 📦 Endpoints de Lotes (Batches)

### Listar Lotes

```http
GET /api/batches/
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "product": 1,
    "quantity_received": 100,
    "quantity_available": 87,
    "purchase_price": "10.50",
    "expiration_date": "2025-12-31",
    "received_at": "2024-01-15T10:30:00Z",
    "supplier": "Tech Supplier"
  }
]
```

---

### Crear Lote

```http
POST /api/batches/
Content-Type: application/json
```

**Body:**
```json
{
  "product": 1,
  "quantity_received": 100,
  "quantity_available": 100,
  "purchase_price": "10.50",
  "expiration_date": "2025-12-31",
  "supplier": "Tech Supplier"
}
```

---

### Obtener Lote por ID

```http
GET /api/batches/{id}/
```

---

### Actualizar Lote

```http
PUT /api/batches/{id}/
PATCH /api/batches/{id}/
```

---

### Eliminar Lote

```http
DELETE /api/batches/{id}/
```

---

## 🔄 Endpoints de Movimientos

### Listar Movimientos

```http
GET /api/movements/
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "batch": 1,
    "movement_type": "OUT",
    "quantity": 10,
    "created_at": "2024-01-16T14:30:00Z",
    "note": "Venta a cliente A"
  }
]
```

---

### Crear Movimiento

```http
POST /api/movements/
Content-Type: application/json
```

**Body:**
```json
{
  "batch": 1,
  "movement_type": "OUT",
  "quantity": 10,
  "note": "Venta a cliente A"
}
```

**Tipos Válidos:**
- `"IN"` - Entrada
- `"OUT"` - Salida
- `"ADJUST"` - Ajuste
- `"EXPIRED"` - Expirado

---

### Obtener Movimiento por ID

```http
GET /api/movements/{id}/
```

---

### Actualizar Movimiento

```http
PUT /api/movements/{id}/
PATCH /api/movements/{id}/
```

---

### Eliminar Movimiento

```http
DELETE /api/movements/{id}/
```

---

## 👥 Endpoints de Usuarios

### Listar Perfiles

```http
GET /api/profiles/
```

---

### Obtener Perfil por ID

```http
GET /api/profiles/{id}/
```

---

### Crear Perfil

```http
POST /api/profiles/
Content-Type: application/json
```

**Body:**
```json
{
  "user": 1,
  "company": 1,
  "role": "SELLER"
}
```

---

## 🏢 Endpoints de Empresas

### Listar Empresas

```http
GET /api/companies/
```

---

### Obtener Empresa por ID

```http
GET /api/companies/{id}/
```

---

### Crear Empresa

```http
POST /api/companies/
Content-Type: application/json
```

**Body:**
```json
{
  "name": "Mi Empresa"
}
```

---

## 📊 Casos de Uso Comunes

### 1. Crear Producto en una Empresa

```bash
# 1. Obtener token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# 2. Crear categoría
curl -X POST http://localhost:8000/api/categories/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electrónica",
    "slug": "electronica",
    "company": 1
  }'

# 3. Crear producto
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "slug": "laptop",
    "category": 1,
    "supplier": "Tech Corp",
    "company": 1
  }'
```

---

### 2. Registrar Entrada de Inventario

```bash
# 1. Crear lote (recibir mercancía)
curl -X POST http://localhost:8000/api/batches/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "quantity_received": 50,
    "quantity_available": 50,
    "purchase_price": "500.00",
    "expiration_date": "2025-12-31",
    "supplier": "Tech Corp"
  }'

# 2. Registrar movimiento IN (opcional, si el stock no se actualiza automáticamente)
curl -X POST http://localhost:8000/api/movements/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "batch": 1,
    "movement_type": "IN",
    "quantity": 50,
    "note": "Recepción de mercancía"
  }'
```

---

### 3. Registrar Salida de Producto

```bash
curl -X POST http://localhost:8000/api/movements/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "batch": 1,
    "movement_type": "OUT",
    "quantity": 10,
    "note": "Venta a cliente X"
  }'
```

---

### 4. Registrar Producto Vencido

```bash
curl -X POST http://localhost:8000/api/movements/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "batch": 1,
    "movement_type": "EXPIRED",
    "quantity": 2,
    "note": "Producto vencido 2025-12-31"
  }'
```

---

## 🔍 Filtrado de Resultados

Todos los endpoints GET soportan filtrado por query parameters:

```bash
GET /api/products/?name=Laptop&supplier=Tech%20Corp
GET /api/batches/?product=1
GET /api/movements/?batch=1&movement_type=OUT
```

---

## 📄 Códigos de Estado HTTP

| Código | Significado | Descripción |
|--------|-------------|-------------|
| **200** | OK | Solicitud exitosa |
| **201** | Created | Recurso creado exitosamente |
| **204** | No Content | Solicitud exitosa (sin contenido) |
| **400** | Bad Request | Datos inválidos |
| **401** | Unauthorized | No autenticado |
| **403** | Forbidden | Acceso denegado |
| **404** | Not Found | Recurso no encontrado |
| **500** | Server Error | Error interno del servidor |

---

## 🔒 Notas de Seguridad

1. **Siempre usar HTTPS en producción**
2. **No expongas tokens JWT en URLs**
3. **Almacena tokens de forma segura (localStorage/sessionStorage)**
4. **Rota tokens regularmente**
5. **Valida todos los inputs del cliente**
6. **Usa CORS correctamente**

---

## 📚 Ejemplos Postman

Ver archivo de colección Postman en el repositorio para ejemplos listos para importar.

---

**Última actualización**: 10 de febrero de 2026
