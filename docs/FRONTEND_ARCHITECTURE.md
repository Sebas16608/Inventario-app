# Arquitectura del Frontend

Documentación completa de la arquitectura del frontend de Inventario-app.

## 📐 Estructura General

```
frontend/
├── app/                      # Next.js App Router (páginas)
│   ├── layout.tsx            # Layout raíz
│   ├── page.tsx              # Home page
│   ├── login/                # Página de login
│   ├── register/             # Página de registro
│   ├── dashboard/            # Dashboard principal
│   ├── categories/           # CRUD Categorías
│   ├── products/             # CRUD Productos
│   ├── batches/              # CRUD Lotes
│   ├── movements/            # CRUD Movimientos
│   ├── layout/               # Componentes de layout
│   │   └── ProtectedLayout.tsx
│   └── globals.css           # Estilos globales
├── components/               # Componentes reutilizables
│   ├── Alert.tsx             # Notificaciones
│   ├── Button.tsx            # Botones
│   ├── Card.tsx              # Contenedores
│   ├── Input.tsx             # Campos de entrada
│   ├── Select.tsx            # Dropdowns
│   ├── Navbar.tsx            # Barra de navegación
│   └── index.ts              # Exports
├── lib/                      # Utilidades
│   ├── api.ts                # Configuración Axios
│   └── hooks.ts              # React Query hooks
├── types/                    # Tipos TypeScript
│   └── index.ts              # Interfaces y tipos
├── hooks/                    # React hooks custom
│   ├── useAuth.ts            # Auth hook
│   └── index.ts              # Exports
├── public/                   # Archivos estáticos
├── next.config.js            # Configuración Next.js
├── tailwind.config.ts        # Configuración Tailwind
├── tsconfig.json             # Configuración TypeScript
├── package.json              # Dependencias
└── README.md                 # Guía rápida
```

## 🔄 Flujo de Datos

```
┌──────────────────────────────────────────────────────────────┐
│ Browser (Client-side)                                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Page Component (batches/page.tsx)                   │   │
│  │  - State: form data, errors                         │   │
│  │  - Hooks: useBatches, useCreateBatch               │   │
│  └─────────────────────────────────────────────────────┘   │
│              │                                               │
│              ▼                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ React Query Hooks (lib/hooks.ts)                    │   │
│  │  - useQuery: GET requests                           │   │
│  │  - useMutation: POST/PUT/DELETE                     │   │
│  │  - queryClient: cache management                    │   │
│  └─────────────────────────────────────────────────────┘   │
│              │                                               │
│              ▼                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Axios Instance (lib/api.ts)                         │   │
│  │  - Request interceptor: añade token                 │   │
│  │  - Response interceptor: maneja 401/refresh         │   │
│  │  - Base URL: http://localhost:8000/api             │   │
│  └─────────────────────────────────────────────────────┘   │
│              │                                               │
│              ▼                                               │
└──────────────────────────────────────────────────────────────┘
│ Network Request                                              │
└──────────────────────────────────────────────────────────────┘
│ Backend API (Django)                                         │
│  - 8000/api/batches/POST                                    │
│  - 8000/api/batches/GET                                     │
│  - etc.                                                      │
└──────────────────────────────────────────────────────────────┘
```

## 🎨 Capas de la Aplicación

### 1. **Pages (app/)**
Componentes principales que manejan rutas.

```tsx
// app/batches/page.tsx
export default function BatchesPage() {
  // 1. Importa hooks
  const { data: batches } = useBatches()
  const createMutation = useCreateBatch()
  
  // 2. Estado local para forms
  const [formData, setFormData] = useState({})
  
  // 3. Maneja eventos
  const handleSubmit = async (e) => {
    await createMutation.mutateAsync(formData)
  }
  
  // 4. Renderiza UI
  return <ProtectedLayout>...</ProtectedLayout>
}
```

### 2. **Hooks (lib/hooks.ts)**
React Query hooks para API calls.

```tsx
export function useBatches() {
  return useQuery({
    queryKey: ['batches'],
    queryFn: async () => {
      const response = await api.get('/batches/')
      return response.data
    },
  })
}

export function useCreateBatch() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (data: BatchCreate) => {
      return api.post('/batches/', data)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['batches'] })
    },
  })
}
```

### 3. **API Client (lib/api.ts)**
Configuración de Axios con interceptores.

```tsx
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
})

// Request interceptor: añade token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor: maneja errores
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Intentar refrescar token
      const refreshToken = localStorage.getItem('refresh_token')
      // ...
    }
    return Promise.reject(error)
  }
)
```

### 4. **Components (components/)**
Componentes UI reutilizables.

```tsx
// components/Button.tsx
export function Button({ variant, isLoading, children, ...props }) {
  return (
    <button
      className={`px-4 py-2 rounded ${variant === 'primary' ? 'bg-blue-600' : ''}`}
      disabled={isLoading}
      {...props}
    >
      {isLoading ? '...' : children}
    </button>
  )
}
```

### 5. **Types (types/index.ts)**
Interfaces TypeScript.

```tsx
export interface Batch {
  id: number
  product: number | Product
  quantity_received: number
  quantity_available: number
  purchase_price: string
  expiration_date: string
  received_at: string
  supplier: string
}

export interface BatchCreate {
  product: number
  quantity_received: number
  quantity_available: number
  purchase_price: string
  expiration_date: string
  supplier: string
}
```

## 🔐 Flujo de Autenticación

```
1. Usuario entra en /register
   ↓
2. POST /auth/register/ con email, contraseña, company_name
   ↓
3. Backend crea User + Company + Profile
   ↓
4. Retorna: { access_token, refresh_token, user }
   ↓
5. Frontend guarda tokens en localStorage
   ↓
6. Redirige a /dashboard
   ↓
7. En cada request, Axios interceptor añade:
   Authorization: Bearer <access_token>
   ↓
8. Si token expira (401), usa refresh_token para obtener nuevo
   ↓
9. Si refresh falla, logout y redirige a /login
```

## 🔄 Ciclo de Vida de un Request

### Crear Batch (POST)

```
1. Usuario hace click en "Crear Lote"
   ↓
2. Se abre formulario
   ↓
3. Usuario completa y hace submit
   ↓
4. handleSubmit valida datos
   ↓
5. createMutation.mutateAsync(batchData)
   ↓
6. Hook llama: api.post('/batches/', batchData)
   ↓
7. Axios interceptor añade token
   ↓
8. POST http://localhost:8000/api/batches/
   ↓
9. Backend procesa en:
   - inventario/views/batch_view.py (POST method)
   - Valida con BatchCreateSerializer
   - Crea record en BD
   ↓
10. Retorna 201 + batch data completo
   ↓
11. Hook onSuccess ejecuta:
    queryClient.invalidateQueries(['batches'])
    ↓
12. useQuery automáticamente refetch datos
   ↓
13. Componente re-renderiza con nuevos datos
   ↓
14. Cierra formulario y muestra success
```

### Leer Batches (GET)

```
1. Página carga: useBatches()
   ↓
2. React Query llama: queryFn
   ↓
3. Axios GET /batches/
   ↓
4. Interceptor añade token JWT
   ↓
5. Backend:
   - BaseCompanyAPIView filtra por empresa
   - SELECT * FROM batches WHERE product.company_id = user.company_id
   ↓
6. Retorna 200 + array de batches
   ↓
7. React Query cachea datos
   ↓
8. Componente renderiza tabla
   ↓
9. Mientras usuario navega, caché se reutiliza
   ↓
10. Si hace 5 minutos+ sin usar, invalidate y refetch
```

## 📊 Estado de la Aplicación

### Local (useState)
```tsx
// Form inputs
const [formData, setFormData] = useState({
  product: '',
  quantity_received: '',
  purchase_price: '',
})

// UI state
const [showForm, setShowForm] = useState(false)
const [submitError, setSubmitError] = useState('')
```

### Server (React Query)
```tsx
// Datos de API
const { data: batches, isLoading, error } = useBatches()

// Mutations
const mutation = useCreateBatch()
// mutation.isPending: boolean
// mutation.isSuccess: boolean
// mutation.error: Error | null
```

### Persistido (localStorage)
```tsx
// Tokens
localStorage.setItem('access_token', '...')
localStorage.setItem('refresh_token', '...')

// User info
localStorage.setItem('user', JSON.stringify(user))
```

## 🎯 Patrones Comunes

### Pattern 1: Mostrar Datos (CRUD Read)

```tsx
import { useBatches } from '@/lib/hooks'

export default function BatchPage() {
  const { data: batches, isLoading, error } = useBatches()
  
  if (isLoading) return <Spinner />
  if (error) return <Alert type="error" />
  
  return (
    <table>
      {batches?.map((batch) => (
        <tr key={batch.id}>
          <td>{batch.product.name}</td>
          <td>{batch.quantity_received}</td>
        </tr>
      ))}
    </table>
  )
}
```

### Pattern 2: Crear Datos (CRUD Create)

```tsx
import { useCreateBatch } from '@/lib/hooks'

export default function CreateBatch() {
  const [formData, setFormData] = useState({})
  const mutation = useCreateBatch()
  
  const handleSubmit = async (e) => {
    e.preventDefault()
    
    try {
      await mutation.mutateAsync(formData)
      toast.success('Creado!')
      closeForm()
    } catch (error) {
      setError(error.message)
    }
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <Input value={formData.product} onChange={...} />
      <Button isLoading={mutation.isPending}>Crear</Button>
    </form>
  )
}
```

### Pattern 3: Editar Datos (CRUD Update)

```tsx
const [editingId, setEditingId] = useState<number | null>(null)
const updateMutation = useUpdateBatch()

const handleEdit = (batch) => {
  setFormData({
    product: batch.product.id,
    quantity_received: batch.quantity_received,
  })
  setEditingId(batch.id)
}

const handleSubmit = async (e) => {
  if (editingId) {
    await updateMutation.mutateAsync({
      id: editingId,
      data: formData,
    })
  }
}
```

### Pattern 4: Eliminar Datos (CRUD Delete)

```tsx
const deleteMutation = useDeleteBatch()

const handleDelete = async (id) => {
  if (confirm('¿Eliminar?')) {
    try {
      await deleteMutation.mutateAsync(id)
      toast.success('Eliminado!')
    } catch {
      toast.error('Error')
    }
  }
}
```

## 🛡️ Manejo de Errores

```tsx
// En hooks
const mutation = useCreateBatch()

// En página
try {
  await mutation.mutateAsync(data)
} catch (error) {
  if (error.response?.data?.product?.[0]) {
    setError('Producto no encontrado')
  } else if (error.response?.data?.error) {
    setError(error.response.data.error)
  } else {
    setError('Error desconocido')
  }
}
```

## 📝 Convenciones

- **Nombres de variables**: camelCase
- **Nombres de archivos**: kebab-case para componentes
- **Tipos**: PascalCase
- **Funciones**: camelCase
- **Exports**: default para páginas, named para componentes
- **Imports**: alias @ para rutas absolutas

## 🚀 Performance

- **React Query** cachea datos automáticamente
- **Next.js** optimiza images y código splitting
- **Tailwind CSS** purga estilos no usados
- **Lazy loading** de rutas con App Router

## 📚 Referencias

- [Next.js Documentation](https://nextjs.org/docs)
- [React Query Documentation](https://tanstack.com/query/latest)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
