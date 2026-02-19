# Estado, Storage y Caché

Documentación completa sobre cómo se gestiona el estado en el frontend.

## 🎯 Niveles de Estado

La aplicación utiliza **tres niveles de estado** con propósitos diferentes:

```
┌─────────────────────────────────────┐
│  1. Local State (useState)           │ UI temporal
├─────────────────────────────────────┤
│  2. Server State (React Query)       │ Datos del backend
├─────────────────────────────────────┤
│  3. Persistent State (localStorage)  │ Datos del usuario
└─────────────────────────────────────┘
```

---

## 1️⃣ Local State con `useState`

### Qué es
Estado temporal que vive solo en el componente, se pierde al recargar.

### Cuándo usar
- Estados de formularios no enviados
- Visibilidad de modales
- Expandir/colapsar elementos
- Búsquedas locales
- Estados de UI (hover, focus, etc)

### No usar para
- Datos del backend
- Datos que necesitan persistir
- Datos que comparten múltiples componentes

### Ejemplo

```tsx
function CategoryForm() {
  const [categoryName, setCategoryName] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    
    try {
      await createCategory({ name: categoryName })
      setCategoryName("")  // Limpiar
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <Input
        value={categoryName}
        onChange={(e) => setCategoryName(e.target.value)}
        disabled={isSubmitting}
      />
      <Button loading={isSubmitting}>Crear</Button>
    </form>
  )
}
```

---

## 2️⃣ Server State con React Query

### Qué es
Estado que viene del backend, React Query lo cachea y sincroniza automáticamente.

### Ventajas
- ✅ Caching automático
- ✅ Deduplicación de requests
- ✅ Actualización automática
- ✅ Sincronización en segundo plano
- ✅ Invalidación inteligente

### Cuándo usar
- Datos de la API
- Listas de productos, categorías, etc
- Información del usuario
- Cualquier dato que venga del servidor

### No usar para
- UI estado (modales, dropdowns)
- Datos temporales del usuario
- Caché de cliente que no requiere sync

### Ejemplo - Lectura

```tsx
import { useQuery } from '@tanstack/react-query'

function ProductList() {
  // Hook personalizado que usa useQuery
  const { data, isLoading, error } = useProducts()

  if (isLoading) return <div>Cargando...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <ul>
      {data?.map(product => (
        <li key={product.id}>{product.name}</li>
      ))}
    </ul>
  )
}
```

### Ejemplo - Escritura

```tsx
import { useMutation, useQueryClient } from '@tanstack/react-query'

function CreateProductForm() {
  const queryClient = useQueryClient()

  const createMutation = useMutation({
    mutationFn: (data: ProductCreate) => 
      api.post('/products/', data),
    
    onSuccess: (newProduct) => {
      // Actualizar caché de forma optimista
      queryClient.setQueryData(
        ['products'],
        (old: Product[]) => [...old, newProduct]
      )
    }
  })

  const handleSubmit = async (data: ProductCreate) => {
    await createMutation.mutateAsync(data)
    // React Query invalidará automáticamente
  }

  return (
    <form onSubmit={handleSubmit}>
      { /* formulario */ }
    </form>
  )
}
```

### Configuración de Caché

```tsx
// En la creación del QueryClient
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Tiempo hasta que datos se consideran "stale"
      staleTime: 1000 * 60 * 5,       // 5 minutos
      
      // Tiempo hasta limpiar datos no usados
      gcTime: 1000 * 60 * 10,         // 10 minutos
      
      // Reintentar fallos
      retry: 1,
      
      // Estado de fondo
      refetchOnWindowFocus: true,     // Revalidar al volver a la ventana
      refetchInterval: false,         // No revalidar constantemente
    },
    mutations: {
      retry: 1
    }
  }
})
```

---

## 3️⃣ Persistent State con localStorage

### Qué es
Estado que persiste en el navegador incluso después de cerrar.

### Cuándo usar
- JWT tokens
- Preferencias del usuario
- Últimas búsquedas
- Filtros guardados
- Tema (claro/oscuro)

### No usar para
- Datos sensibles (especialmente en localStorage)
- Datos que necesitan estar sincronizados
- Datos que ocupan mucho espacio

### Hook para localStorage

```tsx
function useLocalStorage<T>(key: string, initialValue: T) {
  // Leer del localStorage
  const readValue: T = (() => {
    if (typeof window === 'undefined') {
      return initialValue
    }

    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.warn(`Error reading localStorage key "${key}":`, error)
      return initialValue
    }
  })()

  const [storedValue, setStoredValue] = useState(readValue)

  // Actualizar localStorage cuando cambie el valor
  const setValue = useCallback((value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value
      
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(key, JSON.stringify(valueToStore))
      }
      
      setStoredValue(valueToStore)
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error)
    }
  }, [key, storedValue])

  return [storedValue, setValue] as const
}
```

**Uso:**
```tsx
function UserPreferences() {
  const [theme, setTheme] = useLocalStorage('theme', 'light')
  const [language, setLanguage] = useLocalStorage('language', 'es')

  return (
    <div>
      <select value={theme} onChange={(e) => setTheme(e.target.value)}>
        <option>light</option>
        <option>dark</option>
      </select>
      
      <select value={language} onChange={(e) => setLanguage(e.target.value)}>
        <option>es</option>
        <option>en</option>
      </select>
    </div>
  )
}
```

---

## 🔐 Token Management

### Almacenamiento de Tokens

```tsx
// localStorage.ts
const TOKEN_KEY = 'access_token'
const REFRESH_KEY = 'refresh_token'

export function saveTokens(access: string, refresh: string) {
  localStorage.setItem(TOKEN_KEY, access)
  localStorage.setItem(REFRESH_KEY, refresh)
}

export function getAccessToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_KEY)
}

export function clearTokens() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(REFRESH_KEY)
}

export function isAuthenticated(): boolean {
  return getAccessToken() !== null
}
```

### Interceptor de Autenticación

```tsx
// En api.ts
api.interceptors.request.use(
  (config) => {
    const token = getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Si error 401 y no hemos reintentado
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = getRefreshToken()
        const response = await api.post('/auth/token/refresh/', {
          refresh: refreshToken
        })

        const { access } = response.data
        saveTokens(access, refreshToken)

        // Reintentar request original
        originalRequest.headers.Authorization = `Bearer ${access}`
        return api(originalRequest)
      } catch (refreshError) {
        // Refresh falló, limpiar y redirigir a login
        clearTokens()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)
```

---

## 📦 Context para Estado Global

### Cuándo usar Context
- Autenticación del usuario
- Empresa actual
- Tema de la aplicación
- Idioma

### NO usar Context para
- Datos que cambian frecuentemente (usar Zustand/Redux)
- Listas grandes de datos (usar React Query)

### Ejemplo - AuthContext

```tsx
import { createContext, useContext, useEffect, useState } from 'react'

interface AuthContextType {
  user: User | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Verificar si hay token guardado
    if (getAccessToken()) {
      // Obtener datos del usuario
      const verifyAuth = async () => {
        try {
          const response = await api.get('/auth/me/')
          setUser(response.data)
        } catch (error) {
          clearTokens()
        } finally {
          setIsLoading(false)
        }
      }
      verifyAuth()
    } else {
      setIsLoading(false)
    }
  }, [])

  const login = async (email: string, password: string) => {
    const response = await api.post('/auth/login/', { email, password })
    const { access_token, refresh_token, user } = response.data
    
    saveTokens(access_token, refresh_token)
    setUser(user)
  }

  const logout = () => {
    clearTokens()
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{
      user,
      isLoading,
      login,
      logout,
      isAuthenticated: !!user
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider')
  }
  return context
}
```

---

## 🔄 Invalidación de Caché

### Revalidar automáticamente

```tsx
const mutation = useMutation({
  mutationFn: (data) => api.post('/products/', data),
  onSuccess: () => {
    // Revalidar lista de productos
    queryClient.invalidateQueries({
      queryKey: ['products']
    })
  }
})
```

### Actualización optimista

```tsx
const mutation = useMutation({
  mutationFn: (data) => api.put(`/products/${id}`, data),
  onMutate: async (newData) => {
    // Cancelar queries en vuelo
    await queryClient.cancelQueries({ queryKey: ['products'] })

    // Guardar datos antiguos
    const previousData = queryClient.getQueryData(['products'])

    // Actualizar optimistamente
    queryClient.setQueryData(['products'], (old: Product[]) =>
      old.map(p => p.id === id ? { ...p, ...newData } : p)
    )

    return { previousData }
  },
  onError: (err, newData, context) => {
    // Si falla, revertir
    if (context?.previousData) {
      queryClient.setQueryData(['products'], context.previousData)
    }
  },
  onSettled: () => {
    // Revalidar después (optimista falló)
    queryClient.invalidateQueries({ queryKey: ['products'] })
  }
})
```

---

## 📊 Monitorear Estado

### React Query DevTools

```tsx
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

export default function RootLayout() {
  return (
    <>
      {/* ... */}
      {process.env.NODE_ENV === 'development' && (
        <ReactQueryDevtools initialIsOpen={false} />
      )}
    </>
  )
}
```

### Custom Hook para Debug

```tsx
function useDebugValue<T>(value: T, formatter?: (value: T) => string) {
  const debugValue = formatter ? formatter(value) : value
  
  useDebugValue(debugValue)
}

// Uso
function useProducts() {
  const query = useQuery({
    queryKey: ['products'],
    queryFn: () => api.get('/products/').then(r => r.data.results)
  })

  useDebugValue(query.data, data => `${data?.length || 0} productos`)

  return query
}
```

---

## 🎯 Patrón: Estado Combinado

A veces necesitas combinar varios tipos de estado:

```tsx
function ProductDashboard() {
  // 1. Local state para UI
  const [searchTerm, setSearchTerm] = useState("")
  const [isFilterOpen, setIsFilterOpen] = useState(false)

  // 2. Server state vía React Query
  const { data: products, isLoading } = useProducts()

  // 3. Persistent state
  const [sortBy, setSortBy] = useLocalStorage('product-sort', 'name')

  // Combinar y procesar
  const filteredProducts = products?.filter(p =>
    p.name.toLowerCase().includes(searchTerm.toLowerCase())
  )?.sort((a, b) => {
    if (sortBy === 'name') return a.name.localeCompare(b.name)
    if (sortBy === 'price') return a.sale_price - b.sale_price
    return 0
  })

  return (
    <div>
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      
      <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
        <option value="name">Nombre</option>
        <option value="price">Precio</option>
      </select>

      {filteredProducts?.map(p => <ProductCard key={p.id} product={p} />)}
    </div>
  )
}
```

---

## 🚨 Anti-patrones

### ❌ Usar localStorage para datos sensibles
```tsx
// MALO
localStorage.setItem('password', userPassword)
localStorage.setItem('user_id', userId)

// BIEN
sessionStorage.setItem('auth_token', token)  // Se limpia al cerrar
```

### ❌ Sincronizar manualmente
```tsx
// MALO
useEffect(() => {
  const data = await fetch('/api/data')
  setData(data)
}, [dependency])

// BIEN
const { data } = useQuery({
  queryKey: ['data'],
  queryFn: () => fetch('/api/data')
})
```

### ❌ Pasar todo por Context
```tsx
// MALO - Context muy cargado
const AppContext = createContext({
  user,
  products,
  categories,
  movements,
  // 20 más propiedades...
})

// BIEN - Context solo para global
const AuthContext = createContext({ user })
const ThemeContext = createContext({ theme })
// Usar React Query para datos
```

### ❌ localStorage sin validación
```tsx
// MALO
const user = JSON.parse(localStorage.getItem('user'))  // Puede fallar

// BIEN
function getStoredUser(): User | null {
  try {
    const data = localStorage.getItem('user')
    return data ? JSON.parse(data) : null
  } catch (error) {
    console.error('Error parsing user', error)
    return null
  }
}
```

---

## 📋 Checklist de Estado

Al crear un componente que necesita estado, preguntarse:

- [ ] ¿Es estado del servidor? → React Query
- [ ] ¿Necesita persistir? → localStorage
- [ ] ¿Es compartido globalmente? → Context
- [ ] ¿Es solo UI del componente? → useState
- [ ] ¿Cambia frecuentemente? → Zustand (si está en muchos componentes)
- [ ] ¿Necesita ser validado? → Agregar validación
- [ ] ¿Necesita ser sincronizado? → Usar WebSocket o polling

---

## 🔗 Relaciones Entre Estados

```
localStorage (Tokens)
         ↓
    API Interceptor
         ↓
   React Query (Server State)
         ↓
    Components (Local State)
         ↓
     useAuth (Context)
         ↓
    useLocalStorage (Preferences)
```

Flujo de datos:
1. Usuario inicia sesión → Token guardado en localStorage
2. Componente hace request → Interceptor añade token
3. Response → React Query cachea datos
4. Componente usa datos → Local state para UI
5. Cambios → Mutations invalidan caché
6. Caché invalidad → Revalidación automática

Es un sistema cohesivo donde cada parte tiene su propósito.
