# 🔧 Completar la Lógica CRUD

Este documento te muestra cómo completar las operaciones CRUD (Create, Read, Update, Delete) en las diferentes páginas.

## 📝 Ejemplo: Categorías

### Estado Actual

La página `/categories` tiene:
- ✅ UI para crear/editar
- ✅ Query para listar categorías
- ❌ Lógica de POST/PUT/DELETE

### Cómo Completarlo

Reemplaza el contenido de `app/categories/page.tsx` con esto:

```tsx
'use client'

import React, { useState, useCallback } from 'react'
import { useCategories, useCreateCategory, useUpdateCategory, useDeleteCategory } from '@/lib/hooks'
import { ProtectedLayout } from '@/app/layout/ProtectedLayout'
import { Card } from '@/components/Card'
import { Button } from '@/components/Button'
import { Input } from '@/components/Input'
import { Alert } from '@/components/Alert'
import { CategoryCreate } from '@/types'

export default function CategoriesPage() {
  const { data: categories, isLoading, error } = useCategories()
  const createMutation = useCreateCategory()
  const updateMutation = useUpdateCategory()
  const deleteMutation = useDeleteCategory()

  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [formData, setFormData] = useState<CategoryCreate>({ 
    name: '', 
    description: '', 
    slug: '' 
  })
  const [submitError, setSubmitError] = useState('')
  const [successMessage, setSuccessMessage] = useState('')

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleOpenForm = useCallback(() => {
    setFormData({ name: '', description: '', slug: '' })
    setEditingId(null)
    setShowForm(true)
    setSubmitError('')
  }, [])

  const handleEditCategory = useCallback((categoryId: number, categoryData: CategoryCreate) => {
    setFormData(categoryData)
    setEditingId(categoryId)
    setShowForm(true)
    setSubmitError('')
  }, [])

  const handleCloseForm = useCallback(() => {
    setShowForm(false)
    setSubmitError('')
    setSuccessMessage('')
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitError('')
    setSuccessMessage('')

    if (!formData.name || !formData.slug) {
      setSubmitError('Nombre y slug son requeridos')
      return
    }

    try {
      if (editingId) {
        await updateMutation.mutateAsync({
          id: editingId,
          data: formData,
        })
        setSuccessMessage('Categoría actualizada correctamente')
      } else {
        await createMutation.mutateAsync(formData)
        setSuccessMessage('Categoría creada correctamente')
      }
      
      handleCloseForm()
    } catch (err: any) {
      const errorMsg = err.response?.data?.error || 'Error al guardar la categoría'
      setSubmitError(errorMsg)
    }
  }

  const handleDeleteCategory = async (categoryId: number) => {
    if (!confirm('¿Estás seguro de que deseas eliminar esta categoría?')) {
      return
    }

    try {
      await deleteMutation.mutateAsync(categoryId)
      setSuccessMessage('Categoría eliminada correctamente')
    } catch (err: any) {
      const errorMsg = err.response?.data?.error || 'Error al eliminar la categoría'
      setSubmitError(errorMsg)
    }
  }

  const isLoading_Mutations = createMutation.isPending || updateMutation.isPending || deleteMutation.isPending

  return (
    <ProtectedLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Categorías</h1>
          <Button onClick={handleOpenForm} variant="primary" disabled={isLoading_Mutations}>
            + Nueva Categoría
          </Button>
        </div>

        {error && <Alert type="error" message="Error al cargar las categorías" />}
        {successMessage && (
          <Alert 
            type="success" 
            message={successMessage}
            onClose={() => setSuccessMessage('')}
          />
        )}

        {showForm && (
          <Card className="bg-primary-50 border-2 border-primary-200">
            <h2 className="text-xl font-bold mb-4">
              {editingId ? 'Editar' : 'Nueva'} Categoría
            </h2>
            {submitError && (
              <Alert 
                type="error" 
                message={submitError} 
                onClose={() => setSubmitError('')} 
              />
            )}
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                label="Nombre"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="Ej: Electrónica"
                required
                disabled={isLoading_Mutations}
              />
              <Input
                label="Slug"
                name="slug"
                value={formData.slug}
                onChange={handleInputChange}
                placeholder="ej-electronica"
                required
                disabled={isLoading_Mutations}
              />
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Descripción
                </label>
                <textarea
                  name="description"
                  value={formData.description || ''}
                  onChange={handleInputChange}
                  placeholder="Descripción de la categoría"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  rows={4}
                  disabled={isLoading_Mutations}
                />
              </div>
              <div className="flex gap-4">
                <Button 
                  type="submit" 
                  variant="primary" 
                  className="flex-1"
                  isLoading={isLoading_Mutations}
                >
                  {editingId ? 'Actualizar' : 'Crear'}
                </Button>
                <Button
                  type="button"
                  variant="secondary"
                  onClick={handleCloseForm}
                  className="flex-1"
                  disabled={isLoading_Mutations}
                >
                  Cancelar
                </Button>
              </div>
            </form>
          </Card>
        )}

        {isLoading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : categories && categories.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {categories.map((category) => (
              <Card key={category.id}>
                <h3 className="text-lg font-bold">{category.name}</h3>
                <p className="text-gray-600 text-sm mt-2">{category.description}</p>
                <p className="text-gray-500 text-xs mt-2">Slug: {category.slug}</p>
                <div className="flex gap-2 mt-4">
                  <Button
                    size="sm"
                    variant="secondary"
                    onClick={() => handleEditCategory(category.id, category)}
                    disabled={isLoading_Mutations}
                  >
                    Editar
                  </Button>
                  <Button 
                    size="sm" 
                    variant="danger"
                    onClick={() => handleDeleteCategory(category.id)}
                    disabled={isLoading_Mutations}
                  >
                    Eliminar
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        ) : (
          <Card className="text-center py-12">
            <p className="text-gray-600">No hay categorías registradas</p>
          </Card>
        )}
      </div>
    </ProtectedLayout>
  )
}
```

## 🎯 Pasos clave:

1. **Importar las mutaciones:**
   ```typescript
   import { useCreateCategory, useUpdateCategory, useDeleteCategory } from '@/lib/hooks'
   ```

2. **Crear instancias de las mutaciones:**
   ```typescript
   const createMutation = useCreateCategory()
   const updateMutation = useUpdateCategory()
   const deleteMutation = useDeleteCategory()
   ```

3. **Usar en handleSubmit:**
   ```typescript
   if (editingId) {
     await updateMutation.mutateAsync({ id: editingId, data: formData })
   } else {
     await createMutation.mutateAsync(formData)
   }
   ```

4. **Usar en handleDelete:**
   ```typescript
   await deleteMutation.mutateAsync(categoryId)
   ```

## 📦 Lo Mismo para Productos

El patrón es idéntico. En `app/products/page.tsx`:

```typescript
import { 
  useCreateProduct, 
  useUpdateProduct, 
  useDeleteProduct 
} from '@/lib/hooks'

// ... mismo código pero con useCreateProduct, etc.
```

## 🎨 Validación de Formularios (Opcional)

Si quieres validación más robusta, puedes usar React Hook Form:

```typescript
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const categorySchema = z.object({
  name: z.string().min(1, 'Nombre requerido'),
  slug: z.string().min(1, 'Slug requerido'),
  description: z.string().optional(),
})

type CategoryFormData = z.infer<typeof categorySchema>

export default function CategoriesPage() {
  const form = useForm<CategoryFormData>({
    resolver: zodResolver(categorySchema),
  })

  const onSubmit = form.handleSubmit(async (data) => {
    // ... lógica
  })
}
```

## ✨ Adicionales

- **Infinite scroll**: Agregar `useInfiniteQuery` en `lib/hooks.ts`
- **Búsqueda**: Agregar parámetro `search` en las queries
- **Paginación**: Usar `page` en params y mostrar botones
- **Export a CSV**: `npm install papaparse` y exportar

---

¿Necesitas que complete alguna página específica? ¡Solo avisame!
