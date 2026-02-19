# Guía de React Query Hooks

Documentación completa de todos los hooks de React Query para manejar datos de la API.

## 📚 Introducción

React Query maneja:
- **Fetching**: GET requests
- **Caching**: Reutiliza datos automáticamente
- **Synchronization**: Refetch cuando cambian datos
- **Mutations**: POST, PUT, DELETE requests

## 🎯 Categorías

### Lectura de Datos (useQuery)

Los hooks de lectura retornan:
```tsx
{
  data: T | undefined        // Los datos
  isLoading: boolean         // Primer fetch
  isRefetching: boolean      // Refetch en background
  isError: boolean           // Hubo error
  error: Error | null        // Objeto del error
  refetch: () => void        // Refetch manual
}
```

### Escritura de Datos (useMutation)

Los hooks de escritura retornan:
```tsx
{
  isPending: boolean         // Esperando respuesta
  isSuccess: boolean         // Éxito
  isError: boolean           // Error
  error: Error | null        // Objeto del error
  mutate: (data) => void     // Versión sync
  mutateAsync: (data) => Promise // Versión async
}
```

---

## 📦 Hooks Disponibles

### CATEGORÍAS

#### useCategories()
Obtener todas las categorías del usuario.

```tsx
import { useCategories } from '@/lib/hooks'

export function CategoriesPage() {
  const { data: categories, isLoading, error } = useCategories()
  
  return (
    <>
      {isLoading && <p>Cargando...</p>}
      {error && <Alert type="error" />}
      {categories?.map((cat) => (
        <div key={cat.id}>{cat.name}</div>
      ))}
    </>
  )
}
```

**Respuesta:**
```tsx
Category {
  id: number
  name: string
  slug: string          // Para URLs
  description?: string
  company: number       // Solo tu empresa
}
```

#### useCategory(id)
Obtener una categoría específica.

```tsx
const { data: category } = useCategory(1)
```

#### useCreateCategory()
Crear una nueva categoría.

```tsx
const createMutation = useCreateCategory()

const handleCreate = async () => {
  try {
    const newCategory = await createMutation.mutateAsync({
      name: 'Electrónica',
      slug: 'electronica',
      description: 'Categoría de electrónica'
    })
    console.log('Creado:', newCategory)
  } catch (error) {
    console.error('Error:', error)
  }
}
```

**Request:**
```tsx
CategoryCreate {
  name: string          // Requerido
  slug: string          // Requerido, único por empresa
  description?: string
}
```

#### useUpdateCategory()
Actualizar una categoría existente.

```tsx
const updateMutation = useUpdateCategory()

const handleUpdate = async () => {
  await updateMutation.mutateAsync({
    id: 1,
    data: {
      name: 'Nuevo nombre',
      slug: 'nuevo-nombre'
    }
  })
}
```

#### useDeleteCategory()
Eliminar una categoría.

```tsx
const deleteMutation = useDeleteCategory()

const handleDelete = async (id: number) => {
  if (confirm('¿Estás seguro?')) {
    await deleteMutation.mutateAsync(id)
  }
}
```

---

### PRODUCTOS

#### useProducts(categoryId?)
Obtener productos, opcionalmente filtrados por categoría.

```tsx
// Todos los productos
const { data: allProducts } = useProducts()

// Solo de una categoría
const { data: electronics } = useProducts(1)
```

#### useProduct(id)
Obtener un producto específico.

```tsx
const { data: product } = useProduct(1)
```

#### useCreateProduct()
Crear un nuevo producto.

```tsx
const createMutation = useCreateProduct()

await createMutation.mutateAsync({
  name: 'iPhone 15',
  slug: 'iphone-15',
  category: 1,
  supplier: 'Apple',
  cost_price: '800.00',
  sale_price: '1000.00'
})
```

#### useUpdateProduct()
Actualizar un producto.

```tsx
const updateMutation = useUpdateProduct()

await updateMutation.mutateAsync({
  id: 1,
  data: {
    name: 'iPhone 15 Pro',
    sale_price: '1099.00'
  }
})
```

#### useDeleteProduct()
Eliminar un producto.

```tsx
const deleteMutation = useDeleteProduct()

await deleteMutation.mutateAsync(1)
```

---

### LOTES (BATCHES)

#### useBatches(productId?)
Obtener todos los lotes, opcionalmente de un producto.

```tsx
// Todos los lotes
const { data: allBatches } = useBatches()

// Lotes de un producto
const { data: productBatches } = useBatches(1)
```

**Respuesta:**
```tsx
Batch {
  id: number
  product: number | Product
  quantity_received: number    // Lo que recibimos
  quantity_available: number   // Lo que queda
  purchase_price: string       // Precio de compra
  expiration_date: string      // YYYY-MM-DD
  supplier: string
  received_at: string          // Fecha de creación
}
```

#### useBatch(id)
Obtener un lote específico.

```tsx
const { data: batch } = useBatch(1)
```

#### useCreateBatch()
Crear un nuevo lote.

```tsx
const createMutation = useCreateBatch()

await createMutation.mutateAsync({
  product: 1,                    // ID del producto
  quantity_received: 100,        // Cantidad recibida
  quantity_available: 100,       // Cantidad disponible
  purchase_price: '10.50',       // Precio de compra
  expiration_date: '2025-12-31', // Fecha vencimiento
  supplier: 'Proveedor X'
})
```

**Validaciones:**
- product: requerido, debe existir
- quantity_received: requerido, > 0
- purchase_price: requerido, formato decimal
- expiration_date: requerido, sea válido

#### useUpdateBatch()
Actualizar un lote.

```tsx
const updateMutation = useUpdateBatch()

await updateMutation.mutateAsync({
  id: 1,
  data: {
    quantity_available: 50,  // Reducir disponible
    supplier: 'Nuevo proveedor'
  }
})
```

#### useDeleteBatch()
Eliminar un lote.

```tsx
const deleteMutation = useDeleteBatch()

await deleteMutation.mutateAsync(1)
```

---

### MOVIMIENTOS

#### useMovements(productId?)
Obtener todos los movimientos, opcionalmente de un producto.

```tsx
// Todos los movimientos
const { data: allMovements } = useMovements()

// Movimientos de un producto
const { data: productMovements } = useMovements(1)
```

**Respuesta:**
```tsx
Movement {
  id: number
  product: number | Product
  batch: number | Batch
  quantity: number
  movement_type: 'IN' | 'OUT'   // Entrada o salida
  reason: string                 // Por qué
  created_at: string
  created_by: number | User
}
```

#### useMovement(id)
Obtener un movimiento específico.

```tsx
const { data: movement } = useMovement(1)
```

#### useCreateMovement()
Crear un nuevo movimiento.

```tsx
const createMutation = useCreateMovement()

await createMutation.mutateAsync({
  batch: 1,                // ID del lote
  product: 1,              // ID del producto
  quantity: 50,            // Cantidad
  movement_type: 'OUT',    // IN (entrada) u OUT (salida)
  reason: 'Venta cliente'  // Razón
})
```

**Tipos de movimiento:**
- `IN`: Entrada (stock aumenta)
- `OUT`: Salida (stock disminuye)

#### useUpdateMovement()
Actualizar un movimiento.

```tsx
const updateMutation = useUpdateMovement()

await updateMutation.mutateAsync({
  id: 1,
  data: {
    quantity: 75,
    reason: 'Devolución parcial'
  }
})
```

#### useDeleteMovement()
Eliminar un movimiento.

```tsx
const deleteMutation = useDeleteMovement()

await deleteMutation.mutateAsync(1)
```

---

## 🔄 Patrones Comunes

### Pattern 1: Cargar y Mostrar Datos

```tsx
import { useProducts } from '@/lib/hooks'

export function ProductsList() {
  const { data: products, isLoading, error } = useProducts()
  
  // 1. Mientras carga
  if (isLoading) {
    return <div className="animate-spin">Cargando...</div>
  }
  
  // 2. Si hay error
  if (error) {
    return <Alert type="error" message="Error al cargar productos" />
  }
  
  // 3. Si no hay datos
  if (!products?.length) {
    return <p>No hay productos</p>
  }
  
  // 4. Mostrar datos
  return (
    <table>
      <tbody>
        {products.map((product) => (
          <tr key={product.id}>
            <td>{product.name}</td>
            <td>{product.supplier}</td>
            <td>${product.sale_price}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
```

### Pattern 2: Crear con Validación

```tsx
import { useCreateBatch } from '@/lib/hooks'

export function CreateBatchForm() {
  const [formData, setFormData] = useState({
    product: '',
    quantity_received: '',
    purchase_price: '',
    expiration_date: '',
  })
  const [error, setError] = useState('')
  const mutation = useCreateBatch()
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    // Validar
    if (!formData.product || !formData.quantity_received) {
      setError('Todos los campos son requeridos')
      return
    }
    
    try {
      // Crear
      await mutation.mutateAsync({
        product: parseInt(formData.product),
        quantity_received: parseInt(formData.quantity_received),
        quantity_available: parseInt(formData.quantity_received),
        purchase_price: formData.purchase_price,
        expiration_date: formData.expiration_date,
        supplier: '',
      })
      
      // Reset
      setFormData({
        product: '',
        quantity_received: '',
        purchase_price: '',
        expiration_date: '',
      })
      
      // Success
      // (Alert de éxito desde parent)
    } catch (err: any) {
      const msg = err.response?.data?.message || 'Error al crear'
      setError(msg)
    }
  }
  
  return (
    <form onSubmit={handleSubmit}>
      {error && <Alert type="error" message={error} />}
      <Input
        label="Producto"
        value={formData.product}
        onChange={(e) => setFormData({...formData, product: e.target.value})}
      />
      <Button type="submit" isLoading={mutation.isPending}>
        Crear
      </Button>
    </form>
  )
}
```

### Pattern 3: CRUD Completo

```tsx
export function BatchesManager() {
  const { data: batches, isLoading } = useBatches()
  const createMutation = useCreateBatch()
  const updateMutation = useUpdateBatch()
  const deleteMutation = useDeleteBatch()
  
  const [editingId, setEditingId] = useState<number | null>(null)
  const [formData, setFormData] = useState({...initialState})
  
  // Create
  const handleCreate = async () => {
    await createMutation.mutateAsync(formData)
    setFormData({...initialState})
  }
  
  // Read
  const handleEdit = (batch: Batch) => {
    setFormData({...batch})
    setEditingId(batch.id)
  }
  
  // Update
  const handleSave = async () => {
    if (editingId) {
      await updateMutation.mutateAsync({
        id: editingId,
        data: formData
      })
      setEditingId(null)
    } else {
      await handleCreate()
    }
  }
  
  // Delete
  const handleDelete = async (id: number) => {
    if (confirm('¿Seguro?')) {
      await deleteMutation.mutateAsync(id)
    }
  }
  
  return (
    <>
      {/* Form */}
      <form onSubmit={(e) => { e.preventDefault(); handleSave() }}>
        {/* Inputs */}
        <Button type="submit" isLoading={createMutation.isPending}>
          {editingId ? 'Actualizar' : 'Crear'}
        </Button>
      </form>
      
      {/* Table */}
      <table>
        <tbody>
          {batches?.map((batch) => (
            <tr key={batch.id}>
              <td>{batch.product}</td>
              <td>
                <Button onClick={() => handleEdit(batch)}>Editar</Button>
                <Button onClick={() => handleDelete(batch.id)}>Eliminar</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}
```

---

## ⚙️ Configuración Avanzada

### Refetch Manual

```tsx
const { refetch } = useProducts()

// Refetch cuando el usuario lo pide
const handleRefresh = () => {
  refetch()
}
```

### Invalidar Caché

```tsx
import { useQueryClient } from '@tanstack/react-query'

const queryClient = useQueryClient()

const handleSync = () => {
  // Invalida todos los batches
  queryClient.invalidateQueries({ queryKey: ['batches'] })
  
  // Invalida un batch específico
  queryClient.invalidateQueries({ queryKey: ['batches', 1] })
}
```

### Polling (Refetch Automático)

```tsx
const { data } = useBatches({
  refetchInterval: 5000, // Cada 5 segundos
})
```

### Stale Time (Cuándo considerar datos antiguos)

```tsx
const { data } = useProducts({
  staleTime: 60 * 1000, // 1 minuto
})
```

---

## 🚨 Manejo de Errores

```tsx
const mutation = useCreateBatch()

try {
  await mutation.mutateAsync(data)
} catch (error: any) {
  // Error de validación
  if (error.response?.data?.product?.[0]) {
    setError('Producto inválido')
  }
  // Error general de API
  else if (error.response?.data?.error) {
    setError(error.response.data.error)
  }
  // Error de red
  else if (!error.response) {
    setError('Error de conexión')
  }
  // Otro error
  else {
    setError('Error desconocido')
  }
}
```

---

## 📊 Hooks Internals

```tsx
// En lib/hooks.ts

export function useCreateBatch() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (data: BatchCreate) => {
      const response = await api.post<Batch>('/batches/', data)
      return response.data
    },
    onSuccess: () => {
      // Auto-refetch después de crear
      queryClient.invalidateQueries({ queryKey: ['batches'] })
      queryClient.invalidateQueries({ queryKey: ['products'] })
    },
  })
}
```

---

## 📝 Buenas Prácticas

1. **Siempre manejo de error**
   ```tsx
   try {
     await mutation.mutateAsync(data)
   } catch (error) {
     setError('Error message')
   }
   ```

2. **Mostrar loading states**
   ```tsx
   <Button isLoading={mutation.isPending}>
     Guardar
   </Button>
   ```

3. **Validar antes de enviar**
   ```tsx
   if (!formData.product) {
     setError('Producto requerido')
     return
   }
   ```

4. **Reset de form después de éxito**
   ```tsx
   await mutation.mutateAsync(data)
   setFormData({...initialState})
   ```

5. **Confirmar eliminaciones**
   ```tsx
   if (confirm('¿Estás seguro?')) {
     await deleteMutation.mutateAsync(id)
   }
   ```
