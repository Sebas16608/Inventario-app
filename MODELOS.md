# Modelos de Datos - Inventario App

## 📋 Descripción General

Esta sección documenta la estructura de todos los modelos de datos de la aplicación, sus campos, relaciones y comportamientos.

---

## 👥 Modelos de Autenticación (accounts)

### 1. Company (Empresa)

Representa una empresa o organización que usa el sistema.

```python
class Company(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Integer | PK - Identificador único |
| `name` | CharField(255) | Nombre de la empresa |
| `created_at` | DateTime | Fecha de creación (autom) |

**Relaciones:**
- **1:N con Profile** - Una empresa tiene múltiples perfiles de usuario
- **1:N con Category** - Una empresa tiene múltiples categorías
- **1:N con Product** - Una empresa tiene múltiples productos

**Metadata:**
- `ordering = ["id"]`

**Métodos:**
- `__str__()` - Retorna: `Company Nombre`

---

### 2. Profile (Perfil de Usuario)

Define el rol y empresa de cada usuario dentro del sistema.

```python
class Profile(models.Model):
    ROLE_CHOICES = [
        ("ADMIN", "Administrador"),
        ("SELLER", "Vendedor"),
        ("WAREHOUSE", "Almacén"),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="profiles")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="SELLER")
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Integer | PK - Identificador único |
| `user` | OneToOneField | Usuario de Django relacionado |
| `company` | ForeignKey | Empresa a la que pertenece |
| `role` | CharField | Rol: ADMIN, SELLER, WAREHOUSE |

**Roles Disponibles:**

| Rol | Descripción | Permisos |
|-----|-------------|----------|
| **ADMIN** | Administrador | Acceso total a la empresa |
| **SELLER** | Vendedor | Puede vender productos |
| **WAREHOUSE** | Almacén | Gestiona inventario |

**Relaciones:**
- **OneToOne con User** (Django built-in)
- **1:N con Company** - Un perfil pertenece a una empresa

**Metadata:**
- `ordering = ["id"]`

**Métodos:**
- `__str__()` - Retorna: `Perfil de {username} de {company} con el rol {role}`

---

## 📦 Modelos de Inventario (inventario)

### 3. Category (Categoría)

Agrupa productos en categorías dentro de una empresa.

```python
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="category")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Integer | PK - Identificador único |
| `name` | CharField(255) | Nombre de la categoría |
| `description` | TextField | Descripción detallada (opcional) |
| `slug` | SlugField | URL-friendly identifier |
| `company` | ForeignKey | Empresa propietaria |
| `created_at` | DateTime | Fecha de creación (autom) |
| `updated_at` | DateTime | Fecha última actualización (autom) |

**Relaciones:**
- **1:N con Product** - Una categoría contiene múltiples productos
- **N:1 con Company** - Múltiples categorías por empresa

**Restricciones Únicas:**
- `Unique(company, slug)` - El slug es único por empresa

**Metadata:**
- `ordering = ["id"]`

**Métodos:**
- `__str__()` - Retorna: `{name}`

**Ejemplos de Categorías:**
- Electrónica
- Ropa
- Alimentos
- Medicinas
- Accesorios

---

### 4. Product (Producto)

Representa un producto disponible en el inventario.

```python
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    presentation = models.CharField(max_length=255, blank=True, null=True)
    supplier = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Integer | PK - Identificador único |
| `category` | ForeignKey | Categoría del producto |
| `name` | CharField(255) | Nombre del producto |
| `slug` | SlugField | URL-friendly identifier |
| `presentation` | CharField(255) | Formato (caja, botella, etc) - Opcional |
| `supplier` | CharField(255) | Proveedor principal |
| `company` | ForeignKey | Empresa propietaria |
| `created_at` | DateTime | Fecha de creación (autom) |
| `updated_at` | DateTime | Fecha última actualización (autom) |

**Relaciones:**
- **1:N con Batch** - Un producto tiene múltiples lotes
- **N:1 con Category** - Pertenece a una categoría
- **N:1 con Company** - Pertenece a una empresa

**Restricciones Únicas:**
- `Unique(company, slug)` - El slug es único por empresa

**Metadata:**
- `ordering = ["id"]`

**Métodos:**
- `__str__()` - Retorna: `Producto {name} de {category.name}`

**Ejemplos:**
```
Producto: iPhone 14
Slug: iphone-14
Categoría: Electrónica
Presentación: Unidad
Proveedor: Apple Inc
```

---

### 5. Batch (Lote)

Representa un lote de compra de un producto con seguimiento de stock.

```python
class Batch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="batches")
    quantity_received = models.IntegerField()
    quantity_available = models.IntegerField()
    purchase_price = models.DecimalField(decimal_places=2, max_digits=10)
    expiration_date = models.DateField()
    received_at = models.DateTimeField(auto_now_add=True)
    supplier = models.CharField(max_length=255)
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Integer | PK - Identificador único |
| `product` | ForeignKey | Producto del lote |
| `quantity_received` | Integer | Cantidad original recibida |
| `quantity_available` | Integer | Cantidad disponible actualmente |
| `purchase_price` | Decimal | Precio unitario de compra |
| `expiration_date` | Date | Fecha de vencimiento |
| `received_at` | DateTime | Fecha recepción (autom) |
| `supplier` | CharField(255) | Proveedor del lote |

**Relaciones:**
- **1:N con Movement** - Un lote registra múltiples movimientos
- **N:1 con Product** - Pertenece a un producto

**Metadata:**
- `ordering = ["id"]`

**Métodos:**
- `__str__()` - Retorna: `De {product.name} hay {quantity_available} y se recibieron {quantity_received}`

**Lógica de Stock:**
```
quantity_available = quantity_received 
                   - salidas (OUT movements)
                   + ajustes (ADJUST movements)
                   - expirados (EXPIRED movements)
```

**Ejemplo de Lote:**
```
Producto: Paracetamol 500mg
Cantidad Recibida: 1000
Cantidad Disponible: 987
Precio Compra: $0.10 (por unidad)
Fecha Vencimiento: 2025-12-31
Proveedor: Farmacéutica XYZ
```

---

### 6. Movement (Movimiento de Inventario)

Registra cada cambio en el inventario de un lote.

```python
class Movement(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="movements")
    
    TYPES = [
        ("IN", "Entrada"),
        ("OUT", "Salida"),
        ("ADJUST", "Ajuste"),
        ("EXPIRED", "Expirado")
    ]
    
    movement_type = models.CharField(max_length=7, choices=TYPES)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Integer | PK - Identificador único |
| `batch` | ForeignKey | Lote afectado |
| `movement_type` | CharField | Tipo: IN, OUT, ADJUST, EXPIRED |
| `quantity` | PositiveInteger | Cantidad movida |
| `created_at` | DateTime | Fecha movimiento (autom) |
| `note` | TextField | Nota/razón del movimiento (opcional) |

**Tipos de Movimiento:**

| Tipo | Código | Descripción | Efecto |
|------|--------|-------------|--------|
| **Entrada** | `IN` | Recepción de mercancía | +quantity |
| **Salida** | `OUT` | Venta o envío | -quantity |
| **Ajuste** | `ADJUST` | Corrección de inventario | +/- quantity |
| **Expirado** | `EXPIRED` | Producto vencido | -quantity |

**Relaciones:**
- **N:1 con Batch** - Pertenece a un lote

**Metadata:**
- `ordering = ["id"]`

**Métodos:**
- `__str__()` - Retorna: `{movement_type}`

**Ejemplos:**
```
Movimiento 1:
- Batch: Paracetamol (ID: 5)
- Tipo: IN (Entrada)
- Cantidad: 500
- Nota: "Restock semanal"

Movimiento 2:
- Batch: Paracetamol (ID: 5)
- Tipo: OUT (Salida)
- Cantidad: 250
- Nota: "Venta a farmacia A"

Movimiento 3:
- Batch: Paracetamol (ID: 5)
- Tipo: EXPIRED (Expirado)
- Cantidad: 3
- Nota: "Producto vencido 2025-12-31"
```

---

## 🔄 Diagrama Entidad-Relación (ER)

```
┌──────────────┐
│   Company    │
└────┬─────────┘
     │
     ├──1:N──────────┐
     │               │
     │               ▼
     │          ┌───────────┐
     │          │  Category │
     │          │           │
     │          │ - name    │
     │          │ - slug    │
     │          │ - company │
     │          └─────┬─────┘
     │                │
     │                │ 1:N
     │                │
     │                ▼
     │          ┌──────────┐
     │          │ Product  │
     │          │          │
     │          │ - name   │
     │          │ - slug   │
     │          │ - company│
     │          └────┬─────┘
     │               │
     │               │ 1:N
     │               │
     │               ▼
     │          ┌───────────┐
     │          │  Batch    │
     │          │           │
     │          │ - qty_rcv │
     │          │ - qty_avl │
     │          │ - price   │
     │          │ - expires │
     │          └────┬──────┘
     │               │
     │               │ 1:N
     │               │
     │               ▼
     │          ┌──────────────┐
     │          │  Movement    │
     │          │              │
     │          │ - type       │
     │          │ - quantity   │
     │          │ - created_at │
     │          └──────────────┘
     │
     └──1:N──────────┐
                     │
                     ▼
              ┌────────────┐
              │  Profile   │
              │            │
              │ - user     │
              │ - role     │
              │ - company  │
              └────────────┘
```

---

## 🔒 Restricciones y Validaciones

### Restricciones a Nivel de Base de Datos:

1. **Unicidad de Slug por Empresa**
   ```python
   Unique(company, slug)  # en Category y Product
   ```
   - Evita productos/categorías con mismo slug en empresa

2. **Foreign Key Cascade**
   - Si se elimina Company → se eliminan todas sus relacionadas
   - Si se elimina Product → se eliminan sus Batches y Movements

3. **Campos Positivos**
   - `Movement.quantity` - Solo números positivos

### Validaciones a Nivel de Aplicación:

1. **Disponibilidad de Stock**
   - `quantity_available` no puede ser negativo
   - Sistema debe validar antes de OUT

2. **Fecha de Vencimiento**
   - Debe ser en el futuro
   - Alertas para fechas próximas

3. **Precios**
   - MaxDigits: 10, DecimalPlaces: 2
   - Máximo: 99,999,999.99

---

## 📊 Ejemplos de Datos

### Ejemplo 1: Farmacia "MedPlus"

```
Company: MedPlus

Category:
- ID: 1, Name: "Medicinas", Slug: "medicinas"
- ID: 2, Name: "Vitaminas", Slug: "vitaminas"

Product:
- ID: 1, Name: "Paracetamol 500mg", Category: 1, Supplier: "Pharma Corp"
- ID: 2, Name: "Vitamina C 1000mg", Category: 2, Supplier: "VitaLife"

Batch (Paracetamol):
- ID: 1, Qty Received: 1000, Qty Available: 987, Price: 0.10, Expires: 2025-12-31

Movement (Paracetamol Batch 1):
- ID: 1, Type: IN, Qty: 1000, Created: 2024-01-15
- ID: 2, Type: OUT, Qty: 10, Created: 2024-01-16
- ID: 3, Type: OUT, Qty: 3, Created: 2024-01-17
```

---

## 🔄 Ciclo de Vida Típico

```
1. Crear Company
   POST /api/companies/
   
2. Crear Category
   POST /api/categories/ {company: 1, name: "Electrónica"}
   
3. Crear Product
   POST /api/products/ {category: 1, name: "Laptop", company: 1}
   
4. Recibir Batch
   POST /api/batches/ {product: 1, quantity_received: 50, purchase_price: 500}
   
5. Registrar Movimiento OUT (Venta)
   POST /api/movements/ {batch: 1, type: OUT, quantity: 10}
   → quantity_available actualiza a 40
   
6. Registrar Ajuste
   POST /api/movements/ {batch: 1, type: ADJUST, quantity: 5, note: "Error conteo"}
   → quantity_available actualiza a 45
```

---

**Última actualización**: 10 de febrero de 2026
