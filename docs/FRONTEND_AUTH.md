# Autenticación Frontend - JWT en Next.js

## Descripción General

El sistema de autenticación frontend utiliza JWT (JSON Web Tokens) con un ciclo completo de tokens de acceso y refresh. El frontend maneja automáticamente la renovación de tokens y proporciona una experiencia de usuario transparente.

## Arquitectura de Autenticación

### Componentes Principales

1. **useAuth Hook** (`frontend/hooks/useAuth.ts`)
   - Hook React para gestionar el estado de autenticación
   - Maneja login, registro, logout y refresh de tokens
   - Almacena tokens en localStorage
   - Proporciona estado isAuthenticated

2. **API Client** (`frontend/lib/api.ts`)
   - Instancia de Axios con interceptores
   - Inyecta automáticamente Bearer token en requests
   - Maneja refresh automático de tokens en caso de expiración
   - Maneja logout automático si refresh falla

3. **Auth API Client** (`frontend/lib/api.ts`)
   - Instancia separada de Axios para endpoints de autenticación
   - baseURL: `http://localhost:8000/auth` (configurable)
   - Usado por useAuth hook para login, register, token refresh

## Flow de Autenticación

### 1. Registro

```typescript
const { register, isLoading, error } = useAuth()

// En vista de registro
await register({
  email: 'user@example.com',
  password: 'securepass123',
  first_name: 'Juan',
  last_name: 'Pérez',
  company: 'Mi Empresa'
})
```

**Respuesta del servidor (200):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "company": "Mi Empresa"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "message": "User registered successfully"
}
```

**¿Qué ocurre automáticamente?**
- Los tokens se guardan en localStorage
  - `access_token`: Token de acceso (1 hora de validez)
  - `refresh_token`: Token de refresh (7 días de validez)
- El usuario se almacena en localStorage
- Se establece el header `Authorization: Bearer {access_token}`
- Se redirige a `/dashboard`

### 2. Login

```typescript
const { login, isLoading, error } = useAuth()

await login({
  email: 'user@example.com',
  password: 'securepass123'
})
```

**Respuesta:** Idéntica al registro

### 3. Acceso a Rutas Protegidas

```typescript
import { useAuth } from '@/hooks/useAuth'

export default function Dashboard() {
  const { isAuthenticated, user, isLoading } = useAuth()

  if (isLoading) return <LoadingSpinner />
  
  if (!isAuthenticated) {
    return <Redirect to="/login" />
  }

  return (
    <div>
      <h1>Bienvenido {user?.first_name}</h1>
      {/* Contenido protegido */}
    </div>
  )
}
```

### 4. Requests a API Protegida

```typescript
import api from '@/lib/api'

// Automáticamente injected: Authorization: Bearer {access_token}
const response = await api.get('/products/')

// También funciona con POST
const response = await api.post('/movements/', {
  product_id: 1,
  quantity: 10,
  type: 'IN'
})
```

### 5. Refresh Automático de Tokens

Cuando el access_token expira (1 hora):

1. **Request falla con 401 Unauthorized**
2. **Interceptor de Axios:**
   - Detecta el 401
   - Obtiene el refresh_token de localStorage
   - Envía POST a `/auth/token/refresh/`
3. **Servidor responde con nuevo access_token**
4. **Interceptor:**
   - Actualiza localStorage
   - Actualiza header Authorization
   - Reintenta el request original
   - Usuario NO es desconectado

**¿Qué puede ir mal?**
- Si refresh_token también expiró (7 días)
  - Interceptor no puede renovar
  - Limpia localStorage
  - Redirige a `/login`
  - Usuario debe hacer login nuevamente

### 6. Logout

```typescript
const { logout } = useAuth()

logout()

// Automáticamente:
// 1. Limpia localStorage (access_token, refresh_token, user)
// 2. Elimina header Authorization
// 3. Redirige a /login
```

## Estructura de Estado del Hook

```typescript
interface AuthState {
  user: User | null              // Datos del usuario autenticado
  accessToken: string | null     // Token de acceso actual
  refreshToken: string | null    // Token de refresh
  isLoading: boolean             // Indicador de carga
  error: string | null           // Mensaje de error
  isAuthenticated: boolean       // True si hay usuario y token válido
}
```

## Métodos del Hook

### login(credentials: LoginCredentials)
- **Parámetros:** `{ email: string, password: string }`
- **Retorna:** Promise
- **Errores:** Lanza excepción con detalle del error
- **Side effects:**
  - Almacena tokens en localStorage
  - Actualiza header Authorization
  - Redirige a /dashboard

### register(data: RegisterData)
- **Parámetros:** Usuario con email, password, nombres, empresa
- **Retorna:** Promise
- **Errores:** Similar a login
- **Side effects:** Idénticos a login

### logout()
- **Parámetros:** Ninguno
- **Retorna:** void
- **Side effects:**
  - Limpia localStorage
  - Limpia header Authorization
  - Redirige a /login

### refreshAccessToken()
- **Parámetros:** Ninguno
- **Retorna:** Promise<boolean>
- **Uso:** Normalmente automático, pero disponible para uso manual
- **Side effects:**
  - Actualiza access_token en state y localStorage
  - Actualiza header Authorization

### clearError()
- **Parámetros:** Ninguno
- **Retorna:** void
- **Uso:** Limpiar mensajes de error en UI

## Variables de Entorno

```bash
# .env.local (frontend)

# URL del backend API (datos)
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# URL del backend AUTH (autenticación)
NEXT_PUBLIC_AUTH_URL=http://localhost:8000/auth
```

En producción:
```bash
NEXT_PUBLIC_API_URL=https://api.tudominio.com/api
NEXT_PUBLIC_AUTH_URL=https://api.tudominio.com/auth
```

## Flujo Completo Detallado

### Diagrama de Autenticación

```
Usuario          Frontend          Backend
  |                 |                 |
  |--- Registro --->|                 |
  |                 |--- POST /auth/register/ -->|
  |                 |<-- access + refresh ------!
  |<--- Redirigir --|
  |                 | (almacena en localStorage)
  |                 |
  |--- Request ---- (con Authorization header)
  |                 |---- GET /api/products/ ---->|
  |                 |<---- Response (200) --------|
  |                 |<-- Datos ------!
  |<--- Mostrar ----|
```

### Diagrama de Refresh Token

```
Usuario          Frontend          Backend
  |                 |                 |
  |--- Esperar ---->| (1 hora)        |
  |                 |                 |
  |--- Request ---->|                 |
  |                 |-- GET /api/... (access_token expirado) -->|
  |                 |<---- 401 Unauthorized ---|
  |                 |                 |
  |                 |-- POST /auth/token/refresh/ -->|
  |                 |  (con refresh_token)          |
  |                 |<-- access_token ---------|
  |                 | (actualiza localStorage)
  |                 |-- GET /api/... (nuevo access) -->|
  |                 |<---- Response (200) -----|
  |<--- Mostrar ----|
```

## Manejo de Errores

### Errores de Login/Registro

```typescript
const { login, error } = useAuth()

try {
  await login(credentials)
} catch (err: any) {
  const message = err.response?.data?.detail || 'Error desconocido'
  // Mostrar error al usuario
  showErrorToast(message)
}
```

### Errores en Requests a API

```typescript
import api from '@/lib/api'

try {
  const data = await api.get('/products/')
} catch (error: any) {
  if (error.response?.status === 401) {
    // Token expirado, el interceptor ya manejó esto
    // Si llegamos aquí es porque refresh también falló
    console.log('Sesión expirada, redirigiendo a login')
  } else if (error.response?.status === 403) {
    console.log('No tienes permisos para esta acción')
  } else if (error.response?.status === 404) {
    console.log('Recurso no encontrado')
  }
}
```

## Almacenamiento de Tokens

**localStorage:**
```javascript
// Después de login/register
localStorage.getItem('access_token')    // eyJ0eXAiOiJKV1Q...
localStorage.getItem('refresh_token')   // eyJ0eXAiOiJKV1Q...
localStorage.getItem('user')            // {"id":1,"email":"..."}
```

**¿Por qué localStorage?**
- Persiste entre recargas de página
- Accesible desde cualquier componente
- Fácil de limpiar en logout

⚠️ **Nota de Seguridad:**
- No guardar tokens en localStorage en aplicaciones muy sensibles
- Para máxima seguridad, usar httpOnly cookies (requiere cambios backend)
- Los tokens en localStorage son vulnerables a XSS
- Implementar CSP (Content Security Policy) para mitigar XSS

## Integración con Componentes

### Componente de Login

```typescript
import { useAuth } from '@/hooks/useAuth'
import { useState } from 'react'

export function LoginForm() {
  const { login, isLoading, error, clearError } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await login({ email, password })
    } catch (err) {
      // Error ya está en state
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {error && (
        <div className="error">
          {error}
          <button onClick={clearError}>Cerrar</button>
        </div>
      )}
      <input
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        disabled={isLoading}
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        disabled={isLoading}
      />
      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Iniciando...' : 'Iniciar Sesión'}
      </button>
    </form>
  )
}
```

### Componente de Navegación Protegida

```typescript
import { useAuth } from '@/hooks/useAuth'
import Link from 'next/link'

export function Navbar() {
  const { isAuthenticated, user, logout } = useAuth()

  return (
    <nav>
      {isAuthenticated ? (
        <>
          <span>Bienvenido, {user?.first_name}</span>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <>
          <Link href="/login">Login</Link>
          <Link href="/register">Registrarse</Link>
        </>
      )}
    </nav>
  )
}
```

### Componente Protegido

```typescript
import { useAuth } from '@/hooks/useAuth'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export function ProtectedPage() {
  const { isAuthenticated, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, isLoading, router])

  if (isLoading) return <LoadingSpinner />
  if (!isAuthenticated) return null

  return <Dashboard />
}
```

## Testing

### Test de Mock del Hook

```typescript
import { useAuth } from '@/hooks/useAuth'
import { renderHook, act } from '@testing-library/react'

describe('useAuth', () => {
  it('debe realizar login correctamente', async () => {
    const { result } = renderHook(() => useAuth())

    await act(async () => {
      await result.current.login({
        email: 'test@example.com',
        password: 'pass123'
      })
    })

    expect(result.current.isAuthenticated).toBe(true)
    expect(result.current.user?.email).toBe('test@example.com')
    expect(localStorage.getItem('access_token')).toBeDefined()
  })
})
```

## Troubleshooting

### "Token inválido" al hacer requests

**Causa:** El token expiró y no se renovó correctamente

**Solución:**
1. Limpiar localStorage: `localStorage.clear()`
2. Reopedir login
3. Verificar que refresh_token es válido en backend

### Cookies vs localStorage

**Situación:** ¿Debo usar cookies?

**Respuesta:** 
- Para aplicaciones básicas: localStorage está bien
- Para aplicaciones muy sensibles (banca): httpOnly cookies
- Para máxima seguridad: cookies + CSRF tokens

### CORS issues

**Error:** "Access to XMLHttpRequest blocked by CORS policy"

**Solución:**
1. Verificar que `CORS_ALLOWED_ORIGINS` en backend incluye tu frontend
2. En desarrollo: `localhost:3000`
3. En producción: tu dominio

## Checklist de Seguridad

- [ ] Tokens no se loguean nunca
- [ ] localStorage no contiene datos sensibles más allá de tokens
- [ ] Content Security Policy implementada
- [ ] HTTPS en producción
- [ ] Refresh token tiene expiración (7 días)
- [ ] Access token tiene expiración corta (1 hora)
- [ ] Logout limpia todos los tokens
- [ ] API rechaza requests sin token o con token inválido

## Referencias

- [JWT.io](https://jwt.io) - Información sobre JWT
- [Django Rest Framework JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Axios Interceptors](https://axios-http.com/docs/interceptors)
- [localStorage MDN](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)
