# Tipos TypeScript

Documentación completa de interfaces y tipos utilizados en el frontend.

## 🏗️ Tipos Base

### User
Usuario autenticado en el sistema.

```tsx
interface User {
  id: number
  email: string
  username: string
  company: number | Company
  profile?: Profile
  role?: string    // 'ADMIN', 'EMPLOYEE', 'VIEWER'
}
```

### Company
Empresa/Organización que usa el sistema.

```tsx
interface Company {
  id: number
  name: string
  created_at: string
}
```

### Profile
Perfil adicional del usuario.

```tsx
interface Profile {
  id: number
  user: number
  bio?: string
  avatar?: string
  phone?: string
  created_at: string
}
```

---

## 📚 Tipos de Inventario

### Category
Categoría de productos.

```tsx
interface Category {
  id: number
  name: string
  slug: string          // URL-friendly, único por empresa
  description?: string
  company: number       // Solo tu empresa
}
```

**Creación:**
```tsx
interface CategoryCreate {
  name: string
  slug: string
  description?: string
}
```

---

### Product
Producto en el inventario.

```tsx
interface Product {
  id: number
  name: string
  slug: string          // Único por empresa
  category: number | Category
  supplier: string
  cost_price: string    // Formato decimal
  sale_price: string    // Formato decimal
  stock: number         // Cantidad en stock
  company: number
  created_at: string
}
```

**Creación:**
```tsx
interface ProductCreate {
  name: string
  slug: string
  category: number      // ID de categoría
  supplier: string
  cost_price: string   // "100.50"
  sale_price: string   // "150.00"
}
```

---

### Batch
Lote/partida de un producto.

```tsx
interface Batch {
  id: number
  product: number | Product
  quantity_received: number      // Cantidad que llegó
  quantity_available: number     // Cantidad disponible
  purchase_price: string         // Precio de compra
  expiration_date: string        // "2025-12-31"
  supplier: string
  received_at: string            // Fecha creación
}
```

**Creación:**
```tsx
interface BatchCreate {
  product: number
  quantity_received: number
  quantity_available: number      // Si no especifica = quantity_received
  purchase_price: string         // "10.50"
  expiration_date: string        // "2025-12-31"
  supplier: string
}
```

---

### Movement
Movimiento de stock (entrada/salida).

```tsx
interface Movement {
  id: number
  product: number | Product
  batch: number | Batch
  quantity: number
  movement_type: 'IN' | 'OUT'    // Entrada o salida
  reason: string                  // Por qué del movimiento
  created_at: string
  created_by: number | User
}
```

**Creación:**
```tsx
interface MovementCreate {
  product: number
  batch: number
  quantity: number
  movement_type: 'IN' | 'OUT'
  reason: string
}
```

---

## 🔐 Tipos de Autenticación

### LoginRequest
Datos para iniciar sesión.

```tsx
interface LoginRequest {
  email?: string | username
  password: string
}
```

### RegisterRequest
Datos para registrar nuevo usuario.

```tsx
interface RegisterRequest {
  email: string
  username: string
  password: string
  company_name: string    // Nombre de la empresa
}
```

### AuthResponse
Respuesta de login/register.

```tsx
interface AuthResponse {
  access_token: string   // JWT token corta duración
  refresh_token: string  // JWT token larga duración
  user: User
}
```

### RefreshTokenRequest
Datos para refrescar token.

```tsx
interface RefreshTokenRequest {
  refresh: string        // El refresh token
}
```

### TokenPayload
Contenido del JWT.

```tsx
interface TokenPayload {
  user_id: number
  username: string
  email: string
  company_id: number
  exp: number           // Timestamp expiracion
  iat: number           // Timestamp creacion
}
```

---

## 📊 Tipos de Respuesta de API

### PaginatedResponse
Respuesta paginada de listas.

```tsx
interface PaginatedResponse<T> {
  count: number
  next: string | null      // URL siguiente página
  previous: string | null  // URL página anterior
  results: T[]             // Datos
}
```

**Uso:**
```tsx
const response = await api.get<PaginatedResponse<Product>>('/products/')
const products = response.data.results
const totalCount = response.data.count
```

---

## 🎯 Tipos de Estado Local

### FormData
Estado de un formulario genérico.

```tsx
interface FormData {
  [key: string]: string | number | boolean
}
```

### ApiError
Error retornado por API.

```tsx
interface ApiError {
  response?: {
    status: number
    data: {
      [key: string]: string[]  // Errores de validación
      error?: string           // Error general
      detail?: string          // Detalle
    }
  }
  message: string
}
```

---

## 🔄 Tipos de Hooks

### UseQueryResult
Resultado de useQuery.

```tsx
interface UseQueryResult<T> {
  data: T | undefined
  isLoading: boolean
  isError: boolean
  error: Error | null
  refetch: () => void
  isFetching: boolean
}
```

### UseMutationResult
Resultado de useMutation.

```tsx
interface UseMutationResult<T, E = Error> {
  mutate: (data: any) => void
  mutateAsync: (data: any) => Promise<T>
  isPending: boolean
  isSuccess: boolean
  isError: boolean
  error: E | null
  data: T | undefined
  reset: () => void
}
```

---

## 📝 Tipos Utilitarios

### HttpMethod
Métodos HTTP.

```tsx
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
```

### SortOrder
Orden de sorted.

```tsx
type SortOrder = 'asc' | 'desc'
```

### FilterOperator
Operadores de filtrado.

```tsx
type FilterOperator = '=' | '<' | '>' | '<=' | '>=' | 'contains' | 'in'
```

### LoadingState
Estados de carga.

```tsx
type LoadingState = 'idle' | 'loading' | 'success' | 'error'
```

---

## 🔗 Asignaciones Comunes

### Crear Variantes
Cuando necesitas crear una variante sin ciertos campos:

```tsx
// ReadOnly
type ProductRead = Readonly<Product>

// Partial (todos los campos opcionales)
type ProductUpdate = Partial<ProductCreate>

// Pick (solo ciertos campos)
type ProductPreview = Pick<Product, 'id' | 'name' | 'supplier'>

// Omit (todos menos ciertos campos)
type ProductBasic = Omit<Product, 'company' | 'created_at'>
```

### Unión de Tipos
Cuando algo puede ser múltiples cosas:

```tsx
// Producto o ID del producto
type ProductRef = Product | number

// Movimiento de entrada o salida
type MovementDirection = 'IN' | 'OUT'

// Estado del formulario
type FormState = 'idle' | 'submitting' | 'success' | 'error'
```

---

## ✅ Type Guards

Funciones para validar tipos en runtime.

```tsx
// Validar que sea User completo
function isUser(obj: any): obj is User {
  return obj?.id && obj?.email && obj?.username
}

// Validar que sea error de API
function isApiError(error: any): error is ApiError {
  return error?.response?.data
}

// Validar que sea número
function isId(value: any): value is number {
  return typeof value === 'number' && value > 0
}

// Validar movimiento válido
function isValidMovementType(type: any): type is 'IN' | 'OUT' {
  return type === 'IN' || type === 'OUT'
}
```

**Uso:**
```tsx
if (isUser(data)) {
  console.log(data.email)  // TypeScript sabe que email existe
}

try {
  await api.post(...)
} catch (error) {
  if (isApiError(error)) {
    console.log(error.response.data.error)
  }
}
```

---

## 🎨 Tipos para Componentes

### ButtonProps
Props para componente Button.

```tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
}
```

### InputProps
Props para componente Input.

```tsx
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
}
```

### SelectProps
Props para componente Select.

```tsx
interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string
  options: Array<{ value: string; label: string }>
  error?: string
}
```

### CardProps
Props para componente Card.

```tsx
interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
}
```

### AlertProps
Props para componente Alert.

```tsx
interface AlertProps {
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
  onClose?: () => void
}
```

---

## 📋 Tipos de Tablas

### TableColumn
Definición de columna de tabla.

```tsx
interface TableColumn<T> {
  key: keyof T
  label: string
  sortable?: boolean
  render?: (value: any) => React.ReactNode
  width?: string
}
```

### TableProps
Props para tabla genérica.

```tsx
interface TableProps<T> {
  data: T[]
  columns: TableColumn<T>[]
  isLoading?: boolean
  onRowClick?: (row: T) => void
  selectable?: boolean
}
```

---

## 🔍 Tipos Extendidos

### Relaciones
Cuando un tipo tiene relaciones anidadas.

```tsx
// Producto con categoría expandida
interface ProductWithCategory extends Product {
  category: Category  // En lugar de number | Category
}

// Movimiento con todos los detalles
interface MovementDetailed extends Movement {
  product: Product    // Expandido
  batch: Batch       // Expandido
  created_by: User   // Expandido
}
```

### Discriminated Unions
Para tipos mutuamente excluyentes.

```tsx
type ApiResponse<T> = 
  | {
      status: 'success'
      data: T
      error?: undefined
    }
  | {
      status: 'error'
      data?: undefined
      error: string
    }

// Uso
const response: ApiResponse<Product> = ...
if (response.status === 'success') {
  console.log(response.data)  // TypeScript sabe que data existe
}
```

---

## 🎯 Enums vs Const

### Const (Recomendado)
```tsx
const MOVEMENT_TYPES = {
  IN: 'IN',
  OUT: 'OUT',
} as const

type MovementType = typeof MOVEMENT_TYPES[keyof typeof MOVEMENT_TYPES]
// Tipo: 'IN' | 'OUT'
```

### Enum (Legado)
```tsx
enum MovementType {
  IN = 'IN',
  OUT = 'OUT',
}

// Uso
const type: MovementType = MovementType.IN
```

---

## 📚 Exportación de Tipos

En `types/index.ts`:

```tsx
// Tipos de Usuario
export type { User, Profile, Company }

// Tipos de Inventario
export type { Category, CategoryCreate }
export type { Product, ProductCreate }
export type { Batch, BatchCreate }
export type { Movement, MovementCreate }

// Tipos de API
export type { ApiError, PaginatedResponse }

// Tipos de Auth
export type { LoginRequest, RegisterRequest, AuthResponse }

// Reutilizable en toda la app
import { User, Product, Batch } from '@/types'
```

---

## ✨ Genéricos Útiles

```tsx
// Hook genérico para cualquier tipo
function useApi<T>(endpoint: string) {
  return useQuery<T>({
    queryKey: [endpoint],
    queryFn: () => api.get(endpoint).then(r => r.data)
  })
}

// Mutation genérica
function useMutateApi<T, E = any>(method: HttpMethod) {
  return useMutation<T, E, any>({
    mutationFn: (data) => api[method.toLowerCase()](endpoint, data)
  })
}

// Component genérico
function Table<T extends { id: number }>(props: TableProps<T>) {
  return <table>...</table>
}
```

---

## 🚀 Strict Mode

Para máxima type safety:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true
  }
}
```

---

## 📝 Buenas Prácticas

1. **Nunca usar `any`**
   ```tsx
   // ❌ MAL
   const data: any = response.data
   
   // ✅ BIEN
   const data: Product = response.data
   ```

2. **Usar type vs interface**
   ```tsx
   // Para objetos simples
   type User = { id: number; name: string }
   
   // Para clases o extensión
   interface Animal { name: string }
   interface Dog extends Animal { breed: string }
   ```

3. **Tipos opcionales vs required**
   ```tsx
   // ✅ BIEN - clara intención
   interface Product {
     name: string       // Requerido
     description?: string // Opcional
   }
   ```

4. **Type guards para seguridad**
   ```tsx
   function processProduct(data: unknown) {
     if (isProduct(data)) {
       // Aquí TypeScript sabe que es Product
     }
   }
   ```
