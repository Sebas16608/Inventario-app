# Guía de Componentes

Documentación completa de todos los componentes reutilizables del frontend.

## 📦 Componentes Incluidos

### 1. Button

Botón versátil para acciones.

**Props:**
```tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
  disabled?: boolean
  onClick?: () => void
  children: React.ReactNode
  type?: 'button' | 'submit' | 'reset'
  className?: string
}
```

**Uso:**
```tsx
import { Button } from '@/components'

// Primary button
<Button variant="primary" onClick={handleClick}>
  Crear
</Button>

// Small danger button
<Button size="sm" variant="danger" isLoading={loading}>
  Eliminar
</Button>

// Submit button
<Button type="submit">
  Guardar
</Button>
```

**Estilos:**
- `primary`: Azul, para acciones principales
- `secondary`: Gris, para acciones secundarias
- `danger`: Rojo, para eliminaciones

**Estados:**
- `isLoading`: Desactiva y muestra spinner
- `disabled`: Desactiva visualmente

---

### 2. Input

Campo de entrada de texto con label.

**Props:**
```tsx
interface InputProps {
  label?: string
  type?: 'text' | 'email' | 'password' | 'number' | 'date'
  value: string
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void
  placeholder?: string
  disabled?: boolean
  required?: boolean
  name?: string
  min?: string | number
  max?: string | number
  step?: string | number
  error?: string
}
```

**Uso:**
```tsx
import { Input } from '@/components'

// Email input
<Input
  label="Email"
  type="email"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  required
/>

// Number input
<Input
  label="Cantidad"
  type="number"
  value={quantity}
  onChange={(e) => setQuantity(e.target.value)}
  min="1"
  required
/>

// Date input
<Input
  label="Fecha de Vencimiento"
  type="date"
  value={expirationDate}
  onChange={(e) => setExpirationDate(e.target.value)}
  required
/>

// With error
<Input
  label="Producto"
  value={product}
  error="Producto requerido"
/>
```

**Características:**
- Label automático encima
- Placeholder gris claro
- Borde azul en focus
- Soporte para todos los tipos de input
- Atributos HTML nativos (min, max, step, etc.)

---

### 3. Select

Dropdown para seleccionar entre opciones.

**Props:**
```tsx
interface SelectProps {
  label?: string
  name?: string
  value: string
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void
  options: Array<{ value: string; label: string }>
  disabled?: boolean
  required?: boolean
  error?: string
}
```

**Uso:**
```tsx
import { Select } from '@/components'

// Product selection
<Select
  label="Producto"
  name="product"
  value={selectedProduct}
  onChange={(e) => setSelectedProduct(e.target.value)}
  options={products.map((p) => ({
    value: String(p.id),
    label: p.name,
  }))}
  required
/>

// Movement type
<Select
  label="Tipo de Movimiento"
  value={movementType}
  onChange={(e) => setMovementType(e.target.value)}
  options={[
    { value: 'IN', label: 'Entrada' },
    { value: 'OUT', label: 'Salida' },
  ]}
  required
/>
```

**Características:**
- Label automático
- Placeholder vacío
- Primera opción selecciono por defecto
- Mapeo fácil de arrays a opciones

---

### 4. Card

Contenedor para agrupar contenido.

**Props:**
```tsx
interface CardProps {
  children: React.ReactNode
  className?: string
}
```

**Uso:**
```tsx
import { Card } from '@/components'

// Card simple
<Card>
  <h2>Título</h2>
  <p>Contenido</p>
</Card>

// Card con clases personalizadas
<Card className="bg-blue-50 border border-blue-200">
  <h2>Formulario</h2>
  <form>...</form>
</Card>

// Card para tabla
<Card>
  <table>...</table>
</Card>
```

**Características:**
- Fondo blanco
- Borde gris claro
- Padding automático
- Esquinas redondeadas
- Sombra suave
- Responsive

---

### 5. Alert

Notificación para mensajes.

**Props:**
```tsx
interface AlertProps {
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
  onClose?: () => void
}
```

**Uso:**
```tsx
import { Alert } from '@/components'

// Error alert
{submitError && (
  <Alert
    type="error"
    message={submitError}
    onClose={() => setSubmitError('')}
  />
)}

// Success (sin close)
<Alert
  type="success"
  message="Guardado exitosamente"
/>

// Warning
<Alert
  type="warning"
  message="Esta acción no se puede deshacer"
/>

// Info
<Alert
  type="info"
  message="Debes crear una categoría primero"
/>
```

**Estilos por tipo:**
- `success`: Verde, icono ✓
- `error`: Rojo, icono ✗
- `warning`: Naranja, icono ⚠
- `info`: Azul, icono i

**Características:**
- Botón de cerrar (si onClose)
- Animación de entrada suave
- Auto-dismiss después de 5s (opcional)

---

### 6. Navbar

Barra de navegación superior.

**Props:**
```tsx
interface NavbarProps {
  user?: User
  onLogout?: () => void
}
```

**Uso:**
```tsx
import { Navbar } from '@/components'

<Navbar user={currentUser} onLogout={handleLogout} />
```

**Características:**
- Logo y nombre de app
- Links a secciones principales
- Dropdown de usuario
- Botón logout
- Responsive con menú mobile
- Activa enlace de ruta actual

**Links:**
- Dashboard
- Categorías
- Productos
- Lotes
- Movimientos
- Perfil/Logout

---

## 🎨 Sistema de Estilos

### Colores

```tsx
// Primario (Azul)
bg-primary-50    // Fondo muy claro
bg-primary-100   // Fondo claro
bg-primary-600   // Color principal
text-primary-600 // Texto principal

// Secundario (Gris)
border-gray-200  // Bordes
bg-gray-50       // Fondos alternos

// Semánticos
bg-green-100/200  // Éxito
bg-red-100/200    // Error
bg-yellow-100     // Warning
```

### Espaciado

```tsx
// Padding
p-2   // Small
p-4   // Medium
p-6   // Large

// Margin
m-2
gap-4 // Entre items

// Espacio vertical
space-y-4 // Entre elementos verticales
space-x-2 // Entre elementos horizontales
```

### Tipografía

```tsx
text-xs      // 12px
text-sm      // 14px
text-base    // 16px
text-lg      // 18px
text-xl      // 20px
text-2xl     // 24px
text-3xl     // 30px

font-normal
font-medium
font-semibold
font-bold
```

---

## 🔄 Composición de Componentes

### Formulario Completo

```tsx
<Card className="bg-blue-50 border-2 border-blue-200">
  <h2 className="text-xl font-bold mb-4">Crear Lote</h2>
  
  {error && (
    <Alert
      type="error"
      message={error}
      onClose={() => setError('')}
    />
  )}
  
  <form onSubmit={handleSubmit} className="space-y-4">
    <Select
      label="Producto"
      value={formData.product}
      onChange={handleChange}
      options={products.map((p) => ({
        value: String(p.id),
        label: p.name,
      }))}
      required
    />
    
    <Input
      label="Cantidad"
      type="number"
      value={formData.quantity}
      onChange={handleChange}
      min="1"
      required
    />
    
    <Input
      label="Precio"
      type="number"
      step="0.01"
      value={formData.price}
      onChange={handleChange}
      required
    />
    
    <div className="flex gap-4">
      <Button
        type="submit"
        variant="primary"
        className="flex-1"
        isLoading={loading}
      >
        Crear
      </Button>
      <Button
        type="button"
        variant="secondary"
        className="flex-1"
        onClick={onCancel}
      >
        Cancelar
      </Button>
    </div>
  </form>
</Card>
```

### Tabla con Acciones

```tsx
<Card>
  <h2 className="text-xl font-bold mb-4">Lotes</h2>
  
  <div className="overflow-x-auto">
    <table className="w-full">
      <thead className="bg-gray-100">
        <tr>
          <th className="px-4 py-2 text-left">Producto</th>
          <th className="px-4 py-2 text-center">Cantidad</th>
          <th className="px-4 py-2 text-right">Acciones</th>
        </tr>
      </thead>
      <tbody>
        {batches.map((batch) => (
          <tr key={batch.id} className="border-b hover:bg-gray-50">
            <td className="px-4 py-3">
              {batch.product.name}
            </td>
            <td className="px-4 py-3 text-center">
              {batch.quantity_received}
            </td>
            <td className="px-4 py-3 text-right space-x-2">
              <Button
                size="sm"
                variant="secondary"
                onClick={() => handleEdit(batch)}
              >
                Editar
              </Button>
              <Button
                size="sm"
                variant="danger"
                onClick={() => handleDelete(batch.id)}
                isLoading={deleting === batch.id}
              >
                Eliminar
              </Button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
</Card>
```

---

## 🧪 Testing Componentes

```tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Button } from '@/components'

describe('Button', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })
  
  it('calls onClick handler', async () => {
    const onClick = jest.fn()
    const user = userEvent.setup()
    
    render(<Button onClick={onClick}>Click</Button>)
    await user.click(screen.getByRole('button'))
    
    expect(onClick).toHaveBeenCalledTimes(1)
  })
  
  it('disables when loading', () => {
    render(<Button isLoading>Click</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })
})
```

---

## 📝 Buenas Prácticas

1. **Siempre pasar className para customizar**
   ```tsx
   <Card className="bg-blue-50">
   ```

2. **Usar labels descriptivos**
   ```tsx
   <Input label="Email del Usuario" />
   ```

3. **Validar errores en client**
   ```tsx
   if (!email) setError('Email requerido')
   ```

4. **Mostrar loading states**
   ```tsx
   <Button isLoading={mutation.isPending}>
     Guardar
   </Button>
   ```

5. **Manejar errores de API**
   ```tsx
   catch (error) {
     setError(error.response?.data?.message || 'Error')
   }
   ```
