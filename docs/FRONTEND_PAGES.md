# Guía de Páginas Frontend

Documentación completa de cada página de la aplicación.

## 🗺️ Mapa de Rutas

```
/                    → Home / Redirect a dashboard
/login               → Página de login
/register            → Registro de usuario + empresa
/dashboard           → Panel principal
/categories          → CRUD de categorías
/products            → CRUD de productos
/batches             → CRUD de lotes
/movements           → CRUD de movimientos
```

---

## 🏠 Home & Layout

### `/` (page.tsx)
Página inicial que redirige según autenticación.

**Lógica:**
```tsx
// Si está autenticado → /dashboard
// Si NO está autenticado → /login
```

**Componentes:**
- Redirección automática
- Valida token en localStorage

---

### Layout Raíz (layout.tsx)
Estructura HTML principal de la app.

**Contenido:**
```tsx
<html>
  <body>
    {children}  // Inyecta página actual
  </body>
</html>
```

**Proporciona:**
- Meta tags (title, description)
- Stylesheets (Tailwind, globals)
- Root providers (QueryClient, auth)

---

## 🔐 Autenticación

### `/login` (app/login/page.tsx)
Página para iniciar sesión.

**Campos:**
```
Email o Usuario
Contraseña
```

**Funcionalidad:**
1. Usuario ingresa credenciales
2. POST `/auth/login/`
3. Backend valida y retorna tokens
4. Frontend guarda: access_token, refresh_token
5. Redirige a `/dashboard`

**Validaciones:**
- Email/usuario: requerido
- Password: requerido, mínimo 6 caracteres

**Errores comunes:**
- "Usuario/contraseña incorrectos"
- "Usuario no existe"
- "Contraseña incorrecta"

**Componentes usados:**
```tsx
<Input type="email" label="Email o Usuario" />
<Input type="password" label="Contraseña" />
<Button type="submit">Iniciar Sesión</Button>
<Link href="/register">¿No tienes cuenta?</Link>
```

**Flujo:**
```
Email/Usuario input
↓
Password input
↓
Click "Iniciar Sesión"
↓
POST /auth/login/
↓
¿Válido?
├─ Sí → localStorage.setItem('access_token', ...)
│        localStorage.setItem('refresh_token', ...)
│        redirect('/dashboard')
└─ No → mostrar error
```

---

### `/register` (app/register/page.tsx)
Página para registrar nuevo usuario y empresa.

**Campos:**
```
Email
Usuario
Contraseña
Empresa (nombre)
```

**Funcionalidad:**
1. Usuario ingresa datos
2. POST `/auth/register/` con email, username, password, company_name
3. Backend crea: User, Company, Profile
4. Retorna tokens
5. Frontend guarda tokens
6. Redirige a `/dashboard`

**Validaciones:**
- Email: requerido, formato válido, único
- Usuario: requerido, único
- Contraseña: requerido, mínimo 6 caracteres
- Empresa: requerido, único

**Errores comunes:**
- "Email ya existe"
- "Usuario ya existe"
- "Empresa ya existe"
- "Contraseña muy simple"

**Componentes usados:**
```tsx
<Input type="email" label="Email" />
<Input label="Usuario" />
<Input type="password" label="Contraseña" />
<Input label="Nombre de tu Empresa" />
<Button type="submit">Registrarse</Button>
<Link href="/login">¿Ya tienes cuenta?</Link>
```

**Flujo:**
```
Email input → validar email único
Usuario input → validar usuario único
Password input
Company input
↓
Click "Registrarse"
↓
POST /auth/register/
↓
Backend crea User + Company
↓
Retorna tokens + user
↓
localStorage.setItem('access_token', ...)
redirect('/dashboard')
```

---

## 📊 Dashboard

### `/dashboard` (app/dashboard/page.tsx)
Panel de control principal con resumen estadístico.

**Secciones:**

#### 1. Tarjetas de Resumen
```
┌────────────┬────────────┬────────────┬────────────┐
│ Productos  │ Categorías │ Lotes      │ Movimientos│
│    15      │     4      │    28      │    120     │
└────────────┴────────────┴────────────┴────────────┘
```

**Datos obtenidos:**
- Total de productos: `useProducts().data?.length`
- Total de categorías: `useCategories().data?.length`
- Total de lotes: `useBatches().data?.length`
- Total de movimientos: `useMovements().data?.length`

**Interactividad:**
- Click en tarjeta → va a sección correspondiente
- Loading spinner si está cargando

#### 2. Últimos Movimientos
```
Tabla con últimos 5 movimientos:
| Producto | Cantidad | Tipo | Fecha      |
|----------|----------|------|------------|
| iPhone   | 50       | OUT  | 19/02/2026 |
```

**Datos:**
```tsx
const movements = useMovements().data?.slice(0, 5)
```

**Estilos:**
- Entrada (IN): Verde
- Salida (OUT): Rojo

#### 3. Acceso Rápido
```
┌─────────────┬──────────────┬────────────┬──────────────┐
│ + Categoría │ + Producto   │ + Lote     │ + Movimiento │
└─────────────┴──────────────┴────────────┴──────────────┘
```

**Links:**
- "Nueva Categoría" → `/categories`
- "Nuevo Producto" → `/products`
- "Nuevo Lote" → `/batches`
- "Movimiento" → `/movements`

**Flujo:**
```
Dashboard carga
↓
useProducts(), useCategories(), useBatches(), useMovements()
↓
Datos en caché o fetching
↓
Tarjetas muestran contadores
↓
Tabla muestra 5 últimos movimientos
↓
Usuario puede hacer click para ir a secciones
```

---

## 📚 Categorías

### `/categories` (app/categories/page.tsx)
Gestión CRUD de categorías.

**Funcionalidad:**

#### Listar
```
Tabla con todas las categorías:
| ID | Nombre | Slug | Acciones |
|----|--------|------|----------|
```

**Datos:**
```tsx
const { data: categories } = useCategories()
```

#### Crear
```
Formulario:
┌──────────────────┐
│ Nombre Categoría │
│ Slug             │
│ [Crear]  [Cancelar] │
└──────────────────┘
```

**Campos:**
- name (string): Nombre de categoría
- slug (string): URL-friendly (ej: "electronica")

**Validación:**
- name: requerido
- slug: requerido, único por empresa

**Código:**
```tsx
const createMutation = useCreateCategory()
await createMutation.mutateAsync({
  name: 'Electrónica',
  slug: 'electronica'
})
```

#### Editar
1. Click en "Editar" de una categoría
2. Abre formulario con datos prefillados
3. User modifica
4. Click "Actualizar"
5. PUT /api/categories/{id}/
6. Tabla se actualiza automáticamente

#### Eliminar
1. Click en "Eliminar"
2. Confirmación: ¿Estás seguro?
3. DELETE /api/categories/{id}/
4. Tabla se actualiza

**Flujo Completo:**
```
1. Página carga → useCategories()
2. Tabla muestra categorías
3. Usuario click "+ Nueva Categoría"
4. Abre formulario
5. Completa name + slug
6. Click "Crear"
7. createMutation.mutateAsync()
8. POST /api/categories/
9. onSuccess: invalidateQueries(['categories'])
10. useCategories() refetch automático
11. Tabla se actualiza
12. Formulario se cierra
```

---

## 📦 Productos

### `/products` (app/products/page.tsx)
Gestión CRUD de productos.

**Estructura:**
Similar a categorías pero con más campos.

**Campos:**
```
name         - string (requerido)
slug         - string (requerido, único)
category     - number (requerido, dropdown)
supplier     - string (requerido)
cost_price   - decimal (requerido)
sale_price   - decimal (requerido)
```

**Validaciones:**
- name: requerido
- slug: requerido, único por empresa
- category: requerido, debe existir
- supplier: requerido
- cost_price: requerido, formato decimal
- sale_price: requerido, formato decimal

**Funcionalidad:**

#### Dropdown de Categorías
```tsx
const { data: categories } = useCategories()
const options = categories?.map(c => ({
  value: String(c.id),
  label: c.name
}))
<Select label="Categoría" options={options} />
```

#### Crear Producto
```tsx
const createMutation = useCreateProduct()
await createMutation.mutateAsync({
  name: 'iPhone 15',
  slug: 'iphone-15',
  category: 1,
  supplier: 'Apple Inc',
  cost_price: '800.00',
  sale_price: '1000.00'
})
```

#### Tabla de Productos
```
| Nombre | Categoría | Proveedor | Precio Venta | Acciones |
|--------|-----------|-----------|--------------|----------|
```

**Flujo:**
```
Producto page carga
↓
useProducts() + useCategories()
↓
Tabla muestra productos
↓
Dropdown selectiona categoría para crear
↓
Usuario completa form + submit
↓
createMutation.mutateAsync()
↓
POST /api/products/
↓
Caché invalida automático
↓
Tabla actualiza
```

---

## 📋 Lotes (Batches)

### `/batches` (app/batches/page.tsx)
Gestión completa de lotes de productos.

**Propósito:**
Rastrear lotes específicos de compra:
- Cantidad recibida vs disponible
- Precio de compra
- Fecha de vencimiento
- Proveedor

**Campos:**
```
product           - number (requerido, dropdown)
quantity_received - number (requerido, > 0)
quantity_available- number (opcional, por defecto = quantity_received)
purchase_price    - string (requerido, decimal)
expiration_date   - date (requerido)
supplier          - string (opcional)
```

**Funcionalidad:**

#### Listar Lotes
```
Tabla:
| Producto | Recibida | Disponible | Precio | Vencimiento | Acciones |
|----------|----------|------------|--------|-------------|----------|
```

**Datos:**
```tsx
const { data: batches } = useBatches()
```

#### Crear Lote
```
Formulario:
┌─────────────────────────────┐
│ Producto (dropdown)          │
│ Cantidad Recibida            │
│ Cantidad Disponible          │
│ Precio de Compra             │
│ Fecha de Vencimiento         │
│ Proveedor (opcional)         │
│ [Crear]  [Cancelar]         │
└─────────────────────────────┘
```

**Ejemplo:**
```tsx
const createMutation = useCreateBatch()
await createMutation.mutateAsync({
  product: 5,
  quantity_received: 100,
  quantity_available: 100,
  purchase_price: '10.50',
  expiration_date: '2025-12-31',
  supplier: 'Distribuidor XYZ'
})
```

#### Editar Lote
```
Modificar cantidad disponible cuando hay salidas
Cambiar proveedor si es necesario
```

#### Eliminar Lote
```
Solo si quantity_available = quantity_received
(O permitir solo si no hay movimientos)
```

**Validaciones:**
- product: requerido
- quantity_received: requerido, > 0
- purchase_price: requerido, formato decimal
- expiration_date: requerido, válido

**Flujo:**
```
Batches page carga
↓
useBatches() + useProducts()
↓
Tabla muestra lotes
↓
User click "+ Nuevo Lote"
↓
Abre formulario
│
├─ Dropdown de productos desde useProducts()
├─ Input cantidad recibida
├─ Input cantidad disponible (opcional)
├─ Input precio compra
├─ Input fecha vencimiento
└─ Input proveedor (opcional)
│
↓
User submit
↓
createMutation.mutateAsync()
↓
POST /api/batches/
│
├─ Backend valida producto pertenece a su empresa
├─ Crea Batch record
└─ Retorna batch creado
│
↓
queryClient.invalidateQueries(['batches'])
↓
useBatches() refetch automático
↓
Tabla actualiza con nuevo lote
↓
Formulario cierra
```

---

## 🔄 Movimientos

### `/movements` (app/movements/page.tsx)
Rastreo de movimientos de stock (entradas/salidas).

**Propósito:**
Historial de cada cambio de stock:
- Entrada de lote (IN)
- Salida a cliente (OUT)
- Ajustes manuales (ADJUST)
- Vencimientos (EXPIRED)

**Campos:**
```
batch         - number (requerido, dropdown)
product       - number (requerido, auto del batch)
quantity      - number (requerido, > 0)
movement_type - 'IN' | 'OUT' (requerido)
reason        - string (descripción del movimiento)
```

**Funcionalidad:**

#### Listar Movimientos
```
Tabla:
| Producto | Lote | Cantidad | Tipo | Razón | Fecha | Acciones |
|----------|------|----------|------|-------|-------|----------|
```

**Datos:**
```tsx
const { data: movements } = useMovements()
```

**Estilos por tipo:**
- IN: Verde (entrada)
- OUT: Rojo (salida)

#### Crear Movimiento
```
Formulario:
┌─────────────────────────────┐
│ Lote (dropdown)              │
│ Tipo Movimiento (IN/OUT)    │
│ Cantidad                     │
│ Razón/Observación (opcional) │
│ [Crear]  [Cancelar]         │
└─────────────────────────────┘
```

**Ejemplo:**
```tsx
const createMutation = useCreateMovement()
await createMutation.mutateAsync({
  batch: 3,
  product: 5,
  quantity: 25,
  movement_type: 'OUT',
  reason: 'Venta al cliente A'
})
```

#### Editar Movimiento
```
Cambiar cantidad o razón
(No cambiar tipo - sería inconsistente)
```

#### Eliminar Movimiento
```
Solo si user es admin (validación en backend)
(Prevenir auditoría incorrecta)
```

**Validaciones:**
- batch: requerido
- quantity: requerido, > 0, <= cantidad disponible
- movement_type: requerido, IN u OUT
- reason: opcional

**Flujo:**
```
Movements page carga
↓
useMovements() + useBatches()
↓
Tabla muestra últimos movimientos
│
├─ Tipo coloreado (IN=verde, OUT=rojo)
└─ Publica en tiem real (última vez)

↓
User click "+ Nuevo Movimiento"
↓
Abre formulario
│
├─ Dropdown batches (del producto de user)
├─ Select movimiento tipo (IN/OUT)
├─ Input cantidad
└─ Input razón
│
↓
User submit
↓
createMutation.mutateAsync()
↓
POST /api/movements/
│
├─ Backend valida:
│  ├─ Batch existe y pertenece a su empresa
│  ├─ Cantidad <= batch.quantity_available (para OUT)
│  └─ Todos los campos requeridos
│
├─ Crea Movement record
└─ Retorna movement creado
│
↓
queryClient.invalidateQueries(['movements'])
queryClient.invalidateQueries(['batches'])
↓
Tablas actualizan
↓
Formulario cierra + success message
```

---

## 🔐 ProtectedLayout

Componente que envuelve todas las páginas protegidas.

**Ubicación:** `app/layout/ProtectedLayout.tsx`

**Funcionalidad:**
```tsx
export function ProtectedLayout({ children }) {
  // 1. Verificar si está autenticado
  const { user, loading } = useAuth()
  
  // 2. Si no está autenticado → redirige a login
  if (!loading && !user) {
    return redirect('/login')
  }
  
  // 3. Si está autenticado → render
  return (
    <div>
      <Navbar user={user} />
      {children}
    </div>
  )
}
```

**Proporciona:**
- Validación de tokens
- Redirección automática
- Navbar con navegación
- Logout

---

## 🔄 Flujo de Navegación

```
┌─────────────────────────────────────────────┐
│ /login o /register                          │
│ (SIN autenticación)                         │
└──────────────┬──────────────────────────────┘
               │ Completa login/register
               │ Recibe tokens
               │
               ▼
┌─────────────────────────────────────────────┐
│ /dashboard (ProtectedLayout)                │
│ ✓ Autenticado                              │
└──────────────┬──────────────────────────────┘
               │ Navigation en Navbar
               │
               ├─→ /categories
               ├─→ /products
               ├─→ /batches
               ├─→ /movements
               └─→ /profile
               
               │ Logout
               ▼
┌─────────────────────────────────────────────┐
│ /login                                      │
│ (tokens removidos)                          │
└─────────────────────────────────────────────┘
```

---

## 📝 Buenas Prácticas

1. **Validar antes de enviar**
   ```tsx
   if (!formData.name) {
     setError('Nombre es requerido')
     return
   }
   ```

2. **Mostrar loading en botones**
   ```tsx
   <Button isLoading={mutation.isPending}>
     Crear
   </Button>
   ```

3. **Manejar errores de API**
   ```tsx
   catch (error) {
     const msg = error.response?.data?.error || 'Error'
     setError(msg)
   }
   ```

4. **Confirmar eliminaciones**
   ```tsx
   if (confirm('¿Estás seguro?')) {
     await deleteMutation.mutateAsync(id)
   }
   ```

5. **Reset de form después de éxito**
   ```tsx
   await mutation.mutateAsync(data)
   setFormData(initialState)
   ```
