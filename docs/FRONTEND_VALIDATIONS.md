# Validaciones de Formularios

Guía completa de validación de datos en formularios del frontend.

## 🎯 Estrategia de Validación

La aplicación utiliza validación en **dos niveles**:

1. **Frontend (Cliente)** - Validación inmediata con feedback al usuario
2. **Backend (Servidor)** - Validación definitiva de datos

---

## 📋 Validación de Autenticación

### Formulario de Login

**Campos:**
```tsx
interface LoginForm {
  email: string    // O username
  password: string
}
```

**Reglas de Validación:**

| Campo | Regla | Mensaje |
|-------|-------|---------|
| email/username | Requerido | "Email o usuario requerido" |
| email | Formato válido | "Email inválido" |
| email | 6-254 caracteres | "Email debe tener 6-254 caracteres" |
| password | Requerido | "Contraseña requerida" |
| password | Mín. 8 caracteres | "Mínimo 8 caracteres" |
| password | Máx. 128 caracteres | "Máximo 128 caracteres" |

**Implementación:**
```tsx
function validateLoginForm(data: Partial<LoginForm>): Record<string, string> {
  const errors: Record<string, string> = {}

  if (!data.email && !data.username) {
    errors.email = "Email o usuario requerido"
  } else if (data.email) {
    // Validar email
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
      errors.email = "Email inválido"
    }
    if (data.email.length < 6 || data.email.length > 254) {
      errors.email = "Email debe tener 6-254 caracteres"
    }
  }

  if (!data.password) {
    errors.password = "Contraseña requerida"
  } else {
    if (data.password.length < 8) {
      errors.password = "Mínimo 8 caracteres"
    }
    if (data.password.length > 128) {
      errors.password = "Máximo 128 caracteres"
    }
  }

  return errors
}
```

---

### Formulario de Registro

**Campos:**
```tsx
interface RegisterForm {
  email: string
  username: string
  password: string
  company_name: string
}
```

**Reglas de Validación:**

| Campo | Regla | Mensaje |
|-------|-------|---------|
| email | Requerido | "Email requerido" |
| email | Válido | "Email inválido" |
| email | 6-254 caracteres | "Email debe tener 6-254 caracteres" |
| username | Requerido | "Usuario requerido" |
| username | 3-50 caracteres | "Usuario debe tener 3-50 caracteres" |
| username | Solo alfanuméricos | "Solo letras, números y _ permitidos" |
| username | Único | "Este usuario ya existe" |
| password | Requerido | "Contraseña requerida" |
| password | Mín. 8 caracteres | "Mínimo 8 caracteres" |
| password | Complejidad | Debe tener mayúscula, número y carácter especial |
| company_name | Requerido | "Nombre de empresa requerido" |
| company_name | 2-100 caracteres | "Empresa debe tener 2-100 caracteres" |

**Implementación:**
```tsx
function validateRegisterForm(data: Partial<RegisterForm>): Record<string, string> {
  const errors: Record<string, string> = {}

  // Email
  if (!data.email) {
    errors.email = "Email requerido"
  } else {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
      errors.email = "Email inválido"
    }
    if (data.email.length < 6 || data.email.length > 254) {
      errors.email = "Email debe tener 6-254 caracteres"
    }
  }

  // Username
  if (!data.username) {
    errors.username = "Usuario requerido"
  } else {
    if (data.username.length < 3 || data.username.length > 50) {
      errors.username = "Usuario debe tener 3-50 caracteres"
    }
    if (!/^[a-zA-Z0-9_]+$/.test(data.username)) {
      errors.username = "Solo letras, números y _ permitidos"
    }
  }

  // Password
  if (!data.password) {
    errors.password = "Contraseña requerida"
  } else {
    if (data.password.length < 8) {
      errors.password = "Mínimo 8 caracteres"
    }
    // Validar complejidad (mayúscula, número, carácter especial)
    if (!/[A-Z]/.test(data.password)) {
      errors.password = "Debe contener al menos una mayúscula"
    }
    if (!/[0-9]/.test(data.password)) {
      errors.password = "Debe contener al menos un número"
    }
    if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(data.password)) {
      errors.password = "Debe contener un carácter especial"
    }
  }

  // Empresa
  if (!data.company_name) {
    errors.company_name = "Nombre de empresa requerido"
  } else {
    if (data.company_name.length < 2 || data.company_name.length > 100) {
      errors.company_name = "Empresa debe tener 2-100 caracteres"
    }
  }

  return errors
}
```

---

## 📦 Validación de Categorías

**Campos:**
```tsx
interface CategoryForm {
  name: string
  slug: string
  description?: string
}
```

**Reglas de Validación:**

| Campo | Regla | Mensaje |
|-------|-------|---------|
| name | Requerido | "Nombre requerido" |
| name | 2-100 caracteres | "Nombre debe tener 2-100 caracteres" |
| name | Único por empresa | "Esta categoría ya existe" |
| slug | Requerido | "Slug requerido" |
| slug | 2-100 caracteres | "Slug debe tener 2-100 caracteres" |
| slug | Solo a-z, 0-9, - | "Solo letras minúsculas, números y guiones" |
| slug | Único por empresa | "Este slug ya existe" |
| description | Máx. 500 caracteres | "Máximo 500 caracteres" |

**Implementación:**
```tsx
function validateCategoryForm(data: Partial<CategoryForm>): Record<string, string> {
  const errors: Record<string, string> = {}

  // Name
  if (!data.name) {
    errors.name = "Nombre requerido"
  } else {
    if (data.name.length < 2 || data.name.length > 100) {
      errors.name = "Nombre debe tener 2-100 caracteres"
    }
  }

  // Slug
  if (!data.slug) {
    errors.slug = "Slug requerido"
  } else {
    if (data.slug.length < 2 || data.slug.length > 100) {
      errors.slug = "Slug debe tener 2-100 caracteres"
    }
    if (!/^[a-z0-9-]+$/.test(data.slug)) {
      errors.slug = "Solo letras minúsculas, números y guiones"
    }
  }

  // Description
  if (data.description && data.description.length > 500) {
    errors.description = "Máximo 500 caracteres"
  }

  return errors
}
```

---

## 🛍️ Validación de Productos

**Campos:**
```tsx
interface ProductForm {
  name: string
  slug: string
  category: number
  supplier: string
  cost_price: string
  sale_price: string
}
```

**Reglas de Validación:**

| Campo | Regla | Mensaje |
|-------|-------|---------|
| name | Requerido | "Nombre requerido" |
| name | 2-200 caracteres | "Nombre debe tener 2-200 caracteres" |
| slug | Requerido | "Slug requerido" |
| slug | Formato válido | "Solo a-z, 0-9, -" |
| category | Requerido | "Categoría requerida" |
| category | Válido | "Debe ser una categoría existente" |
| supplier | Requerido | "Proveedor requerido" |
| supplier | 2-100 caracteres | "Proveedor debe tener 2-100 caracteres" |
| cost_price | Requerido | "Precio de costo requerido" |
| cost_price | Decimal válido | "Formato: X.XX" |
| cost_price | Mayor a 0 | "Debe ser mayor a 0" |
| cost_price | Máximo 999999.99 | "Máximo 999999.99" |
| sale_price | Requerido | "Precio de venta requerido" |
| sale_price | Mayor que cost | "Debe ser mayor al costo" |
| sale_price | Decimal válido | "Formato: X.XX" |

**Implementación:**
```tsx
function validateProductForm(data: Partial<ProductForm>): Record<string, string> {
  const errors: Record<string, string> = {}

  // Name
  if (!data.name) {
    errors.name = "Nombre requerido"
  } else {
    if (data.name.length < 2 || data.name.length > 200) {
      errors.name = "Nombre debe tener 2-200 caracteres"
    }
  }

  // Slug
  if (!data.slug) {
    errors.slug = "Slug requerido"
  } else {
    if (!/^[a-z0-9-]+$/.test(data.slug)) {
      errors.slug = "Solo letras minúsculas, números y guiones"
    }
  }

  // Category
  if (!data.category) {
    errors.category = "Categoría requerida"
  }

  // Supplier
  if (!data.supplier) {
    errors.supplier = "Proveedor requerido"
  } else {
    if (data.supplier.length < 2 || data.supplier.length > 100) {
      errors.supplier = "Proveedor debe tener 2-100 caracteres"
    }
  }

  // Cost Price
  if (!data.cost_price) {
    errors.cost_price = "Precio de costo requerido"
  } else {
    const price = parseFloat(data.cost_price)
    if (isNaN(price)) {
      errors.cost_price = "Formato: X.XX"
    } else if (price <= 0) {
      errors.cost_price = "Debe ser mayor a 0"
    } else if (price > 999999.99) {
      errors.cost_price = "Máximo 999999.99"
    }
  }

  // Sale Price
  if (!data.sale_price) {
    errors.sale_price = "Precio de venta requerido"
  } else {
    const salePrice = parseFloat(data.sale_price)
    const costPrice = parseFloat(data.cost_price || "0")
    if (isNaN(salePrice)) {
      errors.sale_price = "Formato: X.XX"
    } else if (salePrice <= 0) {
      errors.sale_price = "Debe ser mayor a 0"
    } else if (salePrice <= costPrice) {
      errors.sale_price = "Debe ser mayor al costo"
    }
  }

  return errors
}
```

---

## 📦 Validación de Lotes

**Campos:**
```tsx
interface BatchForm {
  product: number
  quantity_received: number
  quantity_available: number
  purchase_price: string
  expiration_date: string
  supplier: string
}
```

**Reglas de Validación:**

| Campo | Regla | Mensaje |
|-------|-------|---------|
| product | Requerido | "Producto requerido" |
| product | Válido | "Debe ser un producto existente" |
| quantity_received | Requerido | "Cantidad recibida requerida" |
| quantity_received | Entero > 0 | "Debe ser un número mayor a 0" |
| quantity_available | Requerido | "Cantidad disponible requerida" |
| quantity_available | <= quantity_received | "No puede exceder cantidad recibida" |
| purchase_price | Requerido | "Precio de compra requerido" |
| purchase_price | Decimal válido | "Formato: X.XX" |
| purchase_price | Mayor a 0 | "Debe ser mayor a 0" |
| expiration_date | Requerido | "Fecha de expiración requerida" |
| expiration_date | Futuro | "Debe ser una fecha futura" |
| expiration_date | Válido | "Formato: YYYY-MM-DD" |
| supplier | Requerido | "Proveedor requerido" |
| supplier | 2-100 caracteres | "Proveedor debe tener 2-100 caracteres" |

**Implementación:**
```tsx
function validateBatchForm(data: Partial<BatchForm>): Record<string, string> {
  const errors: Record<string, string> = {}

  // Product
  if (!data.product) {
    errors.product = "Producto requerido"
  }

  // Quantity Received
  if (!data.quantity_received) {
    errors.quantity_received = "Cantidad recibida requerida"
  } else {
    if (!Number.isInteger(data.quantity_received) || data.quantity_received <= 0) {
      errors.quantity_received = "Debe ser un número entero mayor a 0"
    }
  }

  // Quantity Available
  if (data.quantity_available === undefined) {
    errors.quantity_available = "Cantidad disponible requerida"
  } else {
    if (data.quantity_available > (data.quantity_received || 0)) {
      errors.quantity_available = "No puede exceder cantidad recibida"
    }
  }

  // Purchase Price
  if (!data.purchase_price) {
    errors.purchase_price = "Precio de compra requerido"
  } else {
    const price = parseFloat(data.purchase_price)
    if (isNaN(price)) {
      errors.purchase_price = "Formato: X.XX"
    } else if (price <= 0) {
      errors.purchase_price = "Debe ser mayor a 0"
    }
  }

  // Expiration Date
  if (!data.expiration_date) {
    errors.expiration_date = "Fecha de expiración requerida"
  } else {
    const expDate = new Date(data.expiration_date)
    const today = new Date()
    if (expDate <= today) {
      errors.expiration_date = "Debe ser una fecha futura"
    }
  }

  // Supplier
  if (!data.supplier) {
    errors.supplier = "Proveedor requerido"
  } else {
    if (data.supplier.length < 2 || data.supplier.length > 100) {
      errors.supplier = "Proveedor debe tener 2-100 caracteres"
    }
  }

  return errors
}
```

---

## 📊 Validación de Movimientos

**Campos:**
```tsx
interface MovementForm {
  product: number
  batch: number
  quantity: number
  movement_type: 'IN' | 'OUT'
  reason: string
}
```

**Reglas de Validación:**

| Campo | Regla | Mensaje |
|-------|-------|---------|
| product | Requerido | "Producto requerido" |
| batch | Requerido | "Lote requerido" |
| batch | Válido para producto | "Lote debe ser del producto seleccionado" |
| quantity | Requerido | "Cantidad requerida" |
| quantity | Entero > 0 | "Debe ser un número mayor a 0" |
| quantity | Máximo para salida | "No puede exceder cantidad disponible" |
| movement_type | Requerido | "Tipo de movimiento requerido" |
| movement_type | IN o OUT | "Debe ser entrada (IN) o salida (OUT)" |
| reason | Requerido | "Motivo requerido" |
| reason | 5-250 caracteres | "Motivo debe tener 5-250 caracteres" |

**Implementación:**
```tsx
function validateMovementForm(data: Partial<MovementForm>, batch?: Batch): Record<string, string> {
  const errors: Record<string, string> = {}

  // Product
  if (!data.product) {
    errors.product = "Producto requerido"
  }

  // Batch
  if (!data.batch) {
    errors.batch = "Lote requerido"
  } else {
    if (batch && batch.product !== data.product) {
      errors.batch = "Lote debe ser del producto seleccionado"
    }
  }

  // Quantity
  if (!data.quantity) {
    errors.quantity = "Cantidad requerida"
  } else {
    if (!Number.isInteger(data.quantity) || data.quantity <= 0) {
      errors.quantity = "Debe ser un número entero mayor a 0"
    }
    // Para salidas, validar que no exceda disponible
    if (data.movement_type === 'OUT' && batch) {
      if (data.quantity > batch.quantity_available) {
        errors.quantity = `No puede exceder ${batch.quantity_available} disponibles`
      }
    }
  }

  // Movement Type
  if (!data.movement_type) {
    errors.movement_type = "Tipo de movimiento requerido"
  } else {
    if (data.movement_type !== 'IN' && data.movement_type !== 'OUT') {
      errors.movement_type = "Debe ser entrada (IN) o salida (OUT)"
    }
  }

  // Reason
  if (!data.reason) {
    errors.reason = "Motivo requerido"
  } else {
    if (data.reason.length < 5 || data.reason.length > 250) {
      errors.reason = "Motivo debe tener 5-250 caracteres"
    }
  }

  return errors
}
```

---

## 🔄 Validación en Tiempo Real

### Debouncing
Esperar antes de validar para no saturar:

```tsx
import { useCallback, useRef } from 'react'

function useDebounceValidate(validator: Function, delay: number = 500) {
  const timerRef = useRef<NodeJS.Timeout>()

  return useCallback((data: any) => {
    clearTimeout(timerRef.current)
    timerRef.current = setTimeout(() => {
      validator(data)
    }, delay)
  }, [validator, delay])
}
```

### Validación de Campo Individual

```tsx
function validateField(field: string, value: any, rules: ValidationRules): string {
  const fieldRules = rules[field]
  
  if (!fieldRules) return ""

  for (const rule of fieldRules) {
    const error = rule(value)
    if (error) return error
  }

  return ""
}
```

---

## ✅ Hook de Validación

```tsx
import { useState, useCallback } from 'react'

interface UseFormValidationOptions {
  validator: (data: any) => Record<string, string>
  onValidationComplete?: (errors: Record<string, string>) => void
}

export function useFormValidation(options: UseFormValidationOptions) {
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [touched, setTouched] = useState<Record<string, boolean>>({})

  const validateForm = useCallback((data: any) => {
    const newErrors = options.validator(data)
    setErrors(newErrors)
    options.onValidationComplete?.(newErrors)
    return Object.keys(newErrors).length === 0
  }, [options])

  const validateField = useCallback((field: string, data: any) => {
    const newErrors = options.validator(data)
    setErrors(prev => ({
      ...prev,
      [field]: newErrors[field] || ""
    }))
  }, [options])

  const markFieldTouched = useCallback((field: string) => {
    setTouched(prev => ({
      ...prev,
      [field]: true
    }))
  }, [])

  const clearErrors = useCallback(() => {
    setErrors({})
    setTouched({})
  }, [])

  return {
    errors,
    touched,
    validateForm,
    validateField,
    markFieldTouched,
    clearErrors,
    isValid: Object.keys(errors).length === 0
  }
}
```

**Uso:**
```tsx
const { errors, validateForm, validateField } = useFormValidation({
  validator: validateProductForm
})

const handleSubmit = (data: ProductForm) => {
  if (validateForm(data)) {
    // Enviar a API
  }
}

const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
  validateField(e.target.name, formData)
}
```

---

## 📝 Patrones Comunes

### Validar Email Único
```tsx
async function validateEmailUnique(email: string): Promise<string> {
  try {
    const response = await api.post('/auth/check-email/', { email })
    if (response.data.exists) {
      return "Este email ya está registrado"
    }
  } catch (error) {
    console.error("Error validando email", error)
  }
  return ""
}
```

### Validar Slug Único
```tsx
async function validateSlugUnique(slug: string, exclude?: number): Promise<string> {
  try {
    const response = await api.get('/products/', { params: { slug } })
    if (response.data.results.length > 0) {
      if (exclude && response.data.results[0].id === exclude) {
        return ""  // Es el mismo producto, no hay conflicto
      }
      return "Este slug ya existe"
    }
  } catch (error) {
    console.error("Error validando slug", error)
  }
  return ""
}
```

### Validar Condicionales
```tsx
function validateConditional(data: Partial<ProductForm>): Record<string, string> {
  const errors: Record<string, string> = {}

  // Si el producto es "requiere_control", el proveedor es obligatorio
  if (data.requiresControl && !data.supplier) {
    errors.supplier = "Proveedor obligatorio para productos que requieren control"
  }

  return errors
}
```

---

## 🎯 Mostrar Errores en Componentes

```tsx
// En un Input
<Input
  name="email"
  type="email"
  label="Email"
  value={formData.email}
  onChange={handleChange}
  onBlur={handleBlur}
  error={touched.email ? errors.email : undefined}
/>

// En un Select
<Select
  name="category"
  label="Categoría"
  options={categories}
  value={formData.category}
  onChange={handleChange}
  error={touched.category ? errors.category : undefined}
/>

// Mensaje de error global
{Object.keys(errors).length > 0 && (
  <Alert
    type="error"
    message={`${Object.keys(errors).length} errores en el formulario`}
  />
)}
```

---

## 🚀 Mejor Práctica: Librería de Validación

Si necesitas validaciones complejas, puedes usar **Zod** o **Yup**:

```tsx
import { z } from 'zod'

const productSchema = z.object({
  name: z.string().min(2).max(200),
  slug: z.string().regex(/^[a-z0-9-]+$/),
  category: z.number().positive(),
  supplier: z.string().min(2).max(100),
  cost_price: z.string().refine(val => {
    const num = parseFloat(val)
    return !isNaN(num) && num > 0
  }),
  sale_price: z.string()
})

// Usar
const data = { /* ... */ }
const result = productSchema.safeParse(data)
if (!result.success) {
  console.log(result.error.flatten())
}
```
