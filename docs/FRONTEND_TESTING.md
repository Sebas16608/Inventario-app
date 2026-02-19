# Testing y Buenas Prácticas

Guía de testing y patrones recomendados para el desarrollo del frontend.

## 🧪 Estrategia de Testing

La aplicación utiliza tres niveles de testing:

```
┌─────────────────────────────────┐
│  E2E Tests (Cypress)            │ Pruebas de flujo completo
│  "¿Funciona todo junto?"        │
├─────────────────────────────────┤
│  Integration Tests              │ Pruebas de componentes complejos
│  "¿Funcionan los módulos?"      │
├─────────────────────────────────┤
│  Unit Tests (Jest/Vitest)       │ Pruebas de funciones aisladas
│  "¿Funcionan las partes?"       │
└─────────────────────────────────┘
```

---

## 🧩 Unit Tests

### Probar una Función Validadora

```tsx
// validations.test.ts
import { validateEmail, validatePassword } from '@/lib/validations'

describe('Email Validations', () => {
  it('should validate correct email', () => {
    expect(validateEmail('user@example.com')).toBe('')
  })

  it('should reject invalid email format', () => {
    expect(validateEmail('invalid-email')).toBe('Email inválido')
  })

  it('should reject short email', () => {
    expect(validateEmail('a@b.c')).toBe('Email debe tener 6-254 caracteres')
  })

  it('should reject long email', () => {
    const longEmail = 'a' + '@example.com'.padStart(250, 'x')
    expect(validateEmail(longEmail)).toBe('Email debe tener 6-254 caracteres')
  })
})

describe('Password Validations', () => {
  it('should validate strong password', () => {
    expect(validatePassword('SecurePass123!')).toBe('')
  })

  it('should reject short password', () => {
    expect(validatePassword('Short1!')).toBe('Mínimo 8 caracteres')
  })

  it('should require uppercase letter', () => {
    expect(validatePassword('password123!')).toContain('mayúscula')
  })

  it('should require number', () => {
    expect(validatePassword('Password!')).toContain('número')
  })

  it('should require special character', () => {
    expect(validatePassword('Password123')).toContain('especial')
  })
})
```

### Probar un Hook

```tsx
// useProducts.test.ts
import { renderHook, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useProducts } from '@/hooks'

describe('useProducts', () => {
  it('should fetch products on mount', async () => {
    const queryClient = new QueryClient()
    
    const { result } = renderHook(() => useProducts(), {
      wrapper: ({ children }) => (
        <QueryClientProvider client={queryClient}>
          {children}
        </QueryClientProvider>
      )
    })

    expect(result.current.isLoading).toBe(true)

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(result.current.data).toBeDefined()
    expect(Array.isArray(result.current.data)).toBe(true)
  })

  it('should handle fetch error', async () => {
    // Mock API error
    // ...
  })
})
```

---

## ⚙️ Integration Tests

### Probar un Componente Complejo

```tsx
// ProductForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ProductForm } from '@/components'
import { QueryClientProvider, QueryClient } from '@tanstack/react-query'

describe('ProductForm', () => {
  it('should render form fields', () => {
    render(
      <QueryClientProvider client={new QueryClient()}>
        <ProductForm />
      </QueryClientProvider>
    )

    expect(screen.getByLabelText('Nombre')).toBeInTheDocument()
    expect(screen.getByLabelText('Categoría')).toBeInTheDocument()
    expect(screen.getByLabelText('Precio')).toBeInTheDocument()
  })

  it('should validate required fields', async () => {
    const user = userEvent.setup()
    
    render(
      <QueryClientProvider client={new QueryClient()}>
        <ProductForm />
      </QueryClientProvider>
    )

    const submitBtn = screen.getByRole('button', { name: /crear/i })
    await user.click(submitBtn)

    await waitFor(() => {
      expect(screen.getByText('Nombre requerido')).toBeInTheDocument()
    })
  })

  it('should submit valid form', async () => {
    const user = userEvent.setup()
    const onSubmit = jest.fn()

    render(
      <QueryClientProvider client={new QueryClient()}>
        <ProductForm onSubmit={onSubmit} />
      </QueryClientProvider>
    )

    // Llenar formulario
    await user.type(screen.getByLabelText('Nombre'), 'Producto Test')
    await user.type(screen.getByLabelText('Precio'), '99.99')
    
    await user.click(screen.getByRole('button', { name: /crear/i }))

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalled()
    })
  })

  it('should show loading state during submission', async () => {
    const user = userEvent.setup()

    render(
      <QueryClientProvider client={new QueryClient()}>
        <ProductForm />
      </QueryClientProvider>
    )

    // Llenar y enviar
    await user.type(screen.getByLabelText('Nombre'), 'Test')
    const submitBtn = screen.getByRole('button', { name: /crear/i })
    await user.click(submitBtn)

    expect(submitBtn).toBeDisabled()
  })
})
```

---

## 🎭 E2E Tests (Cypress)

### Flujo de Login

```typescript
// cypress/e2e/auth.cy.ts
describe('Authentication Flow', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login')
  })

  it('should login with valid credentials', () => {
    cy.get('input[name="email"]').type('test@example.com')
    cy.get('input[name="password"]').type('SecurePass123!')
    
    cy.get('button[type="submit"]').click()

    cy.location('pathname').should('eq', '/dashboard')
    cy.get('.navbar').should('contain', 'test@example.com')
  })

  it('should show error with invalid credentials', () => {
    cy.get('input[name="email"]').type('wrong@example.com')
    cy.get('input[name="password"]').type('WrongPassword123!')
    
    cy.get('button[type="submit"]').click()

    cy.get('[role="alert"]').should('contain', 'Email o contraseña incorrecta')
    cy.location('pathname').should('eq', '/login')
  })

  it('should validate required fields', () => {
    cy.get('button[type="submit"]').click()

    cy.get('.error-message').should('have.length', 2)
    cy.get('input[name="email"]').should('have.class', 'error')
    cy.get('input[name="password"]').should('have.class', 'error')
  })
})
```

### Flujo de Productos

```typescript
// cypress/e2e/products.cy.ts
describe('Products Management', () => {
  beforeEach(() => {
    cy.login('test@example.com', 'SecurePass123!')
    cy.visit('http://localhost:3000/products')
  })

  it('should display product list', () => {
    cy.get('table tbody tr').should('have.length.greaterThan', 0)
    cy.get('table tbody tr').first().should('contain', 'Producto')
  })

  it('should create product', () => {
    cy.get('button:contains("Nuevo Producto")').click()

    cy.get('input[name="name"]').type('Producto Test')
    cy.get('input[name="slug"]').type('producto-test')
    cy.get('select[name="category"]').select('1')
    cy.get('input[name="supplier"]').type('Proveedor')
    cy.get('input[name="cost_price"]').type('10.00')
    cy.get('input[name="sale_price"]').type('15.00')

    cy.get('button:contains("Guardar")').click()

    cy.get('[role="alert"]:contains("Creado exitosamente")').should('be.visible')
    cy.get('table tbody').should('contain', 'Producto Test')
  })

  it('should edit product', () => {
    cy.get('table tbody tr').first().within(() => {
      cy.get('button:contains("Editar")').click()
    })

    cy.get('input[name="name"]').clear().type('Producto Actualizado')
    cy.get('button:contains("Guardar")').click()

    cy.get('[role="alert"]:contains("Actualizado exitosamente")').should('be.visible')
  })

  it('should delete product', () => {
    cy.get('table tbody tr').first().within(() => {
      cy.get('button:contains("Eliminar")').click()
    })

    cy.get('[role="dialog"] button:contains("Confirmar")').click()

    cy.get('[role="alert"]:contains("Eliminado exitosamente")').should('be.visible')
  })
})
```

---

## 📝 Mock Data

### Crear Fixtures

```typescript
// cypress/fixtures/products.json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "name": "Laptop",
      "category": 1,
      "supplier": "Dell",
      "cost_price": "500.00",
      "sale_price": "800.00",
      "stock": 10
    },
    {
      "id": 2,
      "name": "Mouse",
      "category": 2,
      "supplier": "Logitech",
      "cost_price": "10.00",
      "sale_price": "15.00",
      "stock": 50
    }
  ]
}
```

### Usar Fixtures en Tests

```typescript
describe('Products', () => {
  beforeEach(() => {
    cy.fixture('products.json').then(data => {
      cy.intercept('GET', '/api/products/', data).as('getProducts')
    })

    cy.visit('/products')
    cy.wait('@getProducts')
  })

  it('should display mocked products', () => {
    cy.get('table tbody tr').should('have.length', 2)
    cy.get('table tbody').should('contain', 'Laptop')
  })
})
```

---

## ✅ Checklist de Testing

### Unit Tests
- [ ] Todas las funciones utilitarias probadas
- [ ] Todas las validaciones probadas con casos positivos y negativos
- [ ] Todos los casos edge case cubiertos
- [ ] Coverage > 80%

### Integration Tests
- [ ] Formularios completos probados
- [ ] Componentes complejos probados
- [ ] Interacciones de usuario simuladas
- [ ] Estados de carga probados

### E2E Tests
- [ ] Flujo de login completo
- [ ] CRUD para cada entidad
- [ ] Errores y validaciones
- [ ] Navegación entre páginas
- [ ] Sincronización con backend

---

## 🐛 Buenas Prácticas de Desarrollo

### 1. Usar TypeScript Correctamente

✅ **DO:**
```tsx
interface User {
  id: number
  email: string
  name: string
}

function GetUser(id: number): Promise<User> {
  return api.get(`/users/${id}`).then(r => r.data)
}
```

❌ **DON'T:**
```tsx
function GetUser(id: any): any {
  return api.get(`/users/${id}`)
}

// O usar unknown sin type guard
function processData(data: unknown) {
  console.log(data.email)  // Error de tipo!
}
```

---

### 2. Manejo de Errores

✅ **DO:**
```tsx
try {
  const response = await api.post('/users', userData)
  return response.data
} catch (error) {
  if (axios.isAxiosError(error)) {
    const message = error.response?.data?.error || 'Error desconocido'
    throw new Error(message)
  }
  throw error
}
```

❌ **DON'T:**
```tsx
// Sin manejo de error
const data = await api.post('/users', userData)

// O ignorar errores
try {
  await api.post('...')
} catch (error) {
  console.log(error)  // Silenciado
}
```

---

### 3. Código Limpio

✅ **DO:**
```tsx
// Nombres descriptivos
const isValidEmail = email => /^.+@.+\..+$/.test(email)
const handleProductCreation = async (data) => { ... }

// Separación de responsabilidades
const validator = validateForm(data)
const api = makeRequest(endpoint, data)

// Single Responsibility
function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: 'EUR'
  }).format(amount)
}
```

❌ **DON'T:**
```tsx
// Nombres genéricos
const x = email => ...
const handler = () => ...

// Todo mezclado
async function do_stuff(e) {
  // Validar, hacer request, formatear todo aquí
}

// Funciones muy grandes
function processOrder() {
  // 200 líneas de lógica
}
```

---

### 4. Composición de Componentes

✅ **DO:**
```tsx
// Componentes pequeños y reutilizables
<ProductForm
  initialData={product}
  onSubmit={handleSave}
  isLoading={isSaving}
  error={error}
/>

// Destructuring de props
interface ProductFormProps {
  initialData?: Product
  onSubmit: (data: ProductCreate) => Promise<void>
  isLoading?: boolean
  error?: string
}

export function ProductForm({ 
  initialData, 
  onSubmit, 
  isLoading = false,
  error 
}: ProductFormProps) {
  // ...
}
```

❌ **DON'T:**
```tsx
// Componentes mega grandes
<Page>
  {/* 500 líneas de lógica */}
</Page>

// Props sin tipo
export function ProductForm(props) {
  const { iData, onSave, loading } = props
  // Confuso y sin autocompletado
}

// Lógica de negocio en componentes
export function Users() {
  const users = await fetch('/api/users')
  // No usar async directamente en componentes
}
```

---

### 5. Performance

✅ **DO:**
```tsx
// Memoizar componentes costosos
const ProductCard = React.memo(({ product }: { product: Product }) => (
  <div>{product.name}</div>
))

// Memoizar callbacks
const handleDelete = useCallback((id: number) => {
  deleteProduct(id)
}, [])

// Lazy loading de rutas
const ProductsPage = lazy(() => import('@/pages/products'))

// useQuery para caché automático
const { data } = useProducts()  // Se cachea automáticamente
```

❌ **DON'T:**
```tsx
// Renderizar todo siempre
{products.map(p => (
  <Product key={p.id} product={p} />  // Se rerenderiza si alguno cambia
))}

// Inline functions en props
<Button onClick={() => console.log('clicked')} />

// Fetch en el componente
function Products() {
  const [data, setData] = useState([])
  useEffect(() => {
    fetch('/api/products').then(...)
  }, [])
}
```

---

### 6. Manejo de Estado

✅ **DO:**
```tsx
// useState solo para UI local
const [isOpen, setIsOpen] = useState(false)

// React Query para servidor
const { data, isLoading } = useProducts()

// localStorage para persistencia
const [token, setToken] = useLocalStorage('token', '')
```

❌ **DON'T:**
```tsx
// Guardar datos del servidor en useState
const [products, setProducts] = useState([])
useEffect(() => {
  api.get('/products').then(setProducts)
}, [])  // Use React Query instead

// Too much state
const [formData, setFormData] = useState({
  name: '', email: '', phone: '',
  address: '', city: '', zip: ''
  // 20 más propiedades
})
```

---

### 7. Documentación

✅ **DO:**
```tsx
/**
 * Valida un email según estándares internacionales
 * @param email - La dirección de email a validar
 * @returns Error message si es inválido, vacío si es válido
 * @example
 * validateEmail('user@example.com')  // retorna ''
 * validateEmail('invalid')           // retorna 'Email inválido'
 */
export function validateEmail(email: string): string {
  // ...
}

// Componentes documentados
interface ButtonProps {
  /** El tamaño del botón */
  size?: 'sm' | 'md' | 'lg'
  /** Variante de color */
  variant?: 'primary' | 'secondary' | 'danger'
  /** Si está en estado de carga */
  isLoading?: boolean
}
```

❌ **DON'T:**
```tsx
// Sin documentación
function ve(e) {
  // qué hace esto?
}

// Comentarios obvios
// Incrementar contador
counter++

// Comentarios desactualizados
// TODO: Arreglar esto en 2022
```

---

### 8. Constantes y Configuración

✅ **DO:**
```tsx
// constants.ts
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL
export const ITEMS_PER_PAGE = 10
export const MAX_FILE_SIZE = 1024 * 1024 * 5  // 5MB

export const MOVEMENT_TYPES = {
  IN: 'IN',
  OUT: 'OUT',
} as const

export const COLORS = {
  primary: '#0ea5e9',
  danger: '#ef4444',
  success: '#22c55e'
} as const

// Usar en componentes
<Button style={{ backgroundColor: COLORS.primary }} />
```

❌ **DON'T:**
```tsx
// Strings mágicos esparcidos
return <div>{status === 'PENDING' ? 'Pendiente' : 'Activo'}</div>

// Números mágicos
const maxItems = 10
const fileSize = 5242880

// URLs hardcodeadas
fetch('https://api.example.com/products')
```

---

## 🎯 Proceso de Revisión de Código

### Antes de Commit

- [ ] Código formateado (prettier)
- [ ] Linter pasa (eslint)
- [ ] TypeScript sin errores
- [ ] Tests pasan
- [ ] Sin `console.log` de debug
- [ ] Sin código comentado muerto

### Antes de Push

- [ ] Build local exitoso
- [ ] Tests E2E pasan
- [ ] Cambios están documentados
- [ ] No hay conflictos con main
- [ ] Rama está actualizada con main

### Code Review Checklist

- [ ] Código es entendible
- [ ] Sigue los patrones del proyecto
- [ ] Tiene tests apropiados
- [ ] Sin duplicación de código
- [ ] Performance considerado
- [ ] Error handling incluido
- [ ] Documentado si es necesario

---

## 🚀 Optimizaciones Comunes

### Lazy Loading de Componentes
```tsx
const Dashboard = lazy(() => import('@/pages/dashboard'))
const Products = lazy(() => import('@/pages/products'))

export function Routes() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/products" element={<Products />} />
      </Routes>
    </Suspense>
  )
}
```

### Code Splitting
```tsx
// next.config.js
module.exports = {
  swcMinify: true,
  compress: true,
}
```

### Imágenes Optimizadas
```tsx
import Image from 'next/image'

<Image
  src="/logo.png"
  alt="Logo"
  width={200}
  height={200}
  priority  // Para imágenes above-the-fold
/>
```

---

## 📊 Métricas de Código

Mantener métricas saludables:

- **Coverage** > 80%
- **Complejidad Ciclomática** < 10
- **Tamaño de función** < 20 líneas (promedio)
- **Duración de tests** < 10s (total)
- **Bundle size** < 500KB

---

## 🔗 Referencias

- [React Best Practices](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Testing Library Docs](https://testing-library.com)
- [Cypress Documentation](https://docs.cypress.io)
- [React Query Docs](https://tanstack.com/query/latest)

---

## ✨ Conclusión

El testing y las buenas prácticas son inversiones que:
- ✅ Reducen bugs en producción
- ✅ Hacen el código más mantenible
- ✅ Facilitan onboarding de nuevos developers
- ✅ Mejoran la confianza en los cambios
- ✅ Ahorran tiempo a largo plazo

Vale la pena dedicar tiempo a escribir tests y código limpio.
