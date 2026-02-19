'use client'

import React, { useState } from 'react'
import { useCategories, useCreateCategory, useUpdateCategory, useDeleteCategory } from '@/lib/hooks'
import { ProtectedLayout } from '@/app/layout/ProtectedLayout'
import { Card } from '@/components/Card'
import { Button } from '@/components/Button'
import { Input } from '@/components/Input'
import { Alert } from '@/components/Alert'

export default function CategoriesPage() {
  const { data: categories, isLoading, error } = useCategories()
  const createMutation = useCreateCategory()
  const updateMutation = useUpdateCategory()
  const deleteMutation = useDeleteCategory()
  
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [formData, setFormData] = useState({ name: '', description: '', slug: '' })
  const [submitError, setSubmitError] = useState('')

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleOpenForm = () => {
    setFormData({ name: '', description: '', slug: '' })
    setEditingId(null)
    setShowForm(true)
  }

  const handleCloseForm = () => {
    setShowForm(false)
    setSubmitError('')
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitError('')

    if (!formData.name.trim() || !formData.slug.trim()) {
      setSubmitError('El nombre y slug son requeridos')
      return
    }

    try {
      if (editingId) {
        await updateMutation.mutateAsync({
          id: editingId,
          data: formData,
        })
      } else {
        await createMutation.mutateAsync(formData)
      }
      handleCloseForm()
    } catch (err: any) {
      const errorMsg = err.response?.data?.name?.[0] || 
                      err.response?.data?.slug?.[0] ||
                      err.response?.data?.error ||
                      'Error al guardar la categoría'
      setSubmitError(errorMsg)
    }
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar esta categoría?')) {
      try {
        await deleteMutation.mutateAsync(id)
      } catch (err: any) {
        setSubmitError('Error al eliminar la categoría')
      }
    }
  }

  return (
    <ProtectedLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Categorías</h1>
          <Button onClick={handleOpenForm} variant="primary">
            + Nueva Categoría
          </Button>
        </div>

        {error && (
          <Alert
            type="error"
            message="Error al cargar las categorías"
          />
        )}

        {showForm && (
          <Card className="bg-primary-50 border-2 border-primary-200">
            <h2 className="text-xl font-bold mb-4">
              {editingId ? 'Editar' : 'Nueva'} Categoría
            </h2>
            {submitError && (
              <Alert type="error" message={submitError} onClose={() => setSubmitError('')} />
            )}
            <form className="space-y-4" onSubmit={handleSubmit}>
              <Input
                label="Nombre"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="Ej: Electrónica"
                required
                disabled={createMutation.isPending || updateMutation.isPending}
              />
              <Input
                label="Slug"
                name="slug"
                value={formData.slug}
                onChange={handleInputChange}
                placeholder="ej-electronica"
                required
                disabled={createMutation.isPending || updateMutation.isPending}
              />
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Descripción
                </label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  placeholder="Descripción de la categoría"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:bg-gray-100"
                  rows={4}
                  disabled={createMutation.isPending || updateMutation.isPending}
                />
              </div>
              <div className="flex gap-4">
                <Button 
                  type="submit" 
                  variant="primary" 
                  className="flex-1"
                  isLoading={createMutation.isPending || updateMutation.isPending}
                >
                  {editingId ? 'Actualizar' : 'Crear'}
                </Button>
                <Button
                  type="button"
                  variant="secondary"
                  onClick={handleCloseForm}
                  className="flex-1"
                  disabled={createMutation.isPending || updateMutation.isPending}
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
                    onClick={() => {
                      setFormData(category)
                      setEditingId(category.id)
                      setShowForm(true)
                    }}
                  >
                    Editar
                  </Button>
                  <Button 
                    size="sm" 
                    variant="danger"
                    onClick={() => handleDelete(category.id)}
                    isLoading={deleteMutation.isPending}
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
