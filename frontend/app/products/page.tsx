'use client'

import React, { useState } from 'react'
import { useProducts, useCategories, useCreateProduct, useUpdateProduct, useDeleteProduct } from '@/lib/hooks'
import { ProtectedLayout } from '@/app/layout/ProtectedLayout'
import { Card } from '@/components/Card'
import { Button } from '@/components/Button'
import { Input } from '@/components/Input'
import { Select } from '@/components/Select'
import { Alert } from '@/components/Alert'

export default function ProductsPage() {
  const { data: products, isLoading, error } = useProducts()
  const { data: categories } = useCategories()
  const createMutation = useCreateProduct()
  const updateMutation = useUpdateProduct()
  const deleteMutation = useDeleteProduct()
  
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    slug: '',
    presentation: '',
    supplier: '',
    category: '',
  })
  const [submitError, setSubmitError] = useState('')

  const categoryOptions = (categories || []).map((cat) => ({
    value: String(cat.id),
    label: cat.name,
  }))

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleOpenForm = () => {
    setFormData({
      name: '',
      slug: '',
      presentation: '',
      supplier: '',
      category: '',
    })
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

    if (!formData.name.trim() || !formData.slug.trim() || !formData.supplier.trim() || !formData.category) {
      setSubmitError('Nombre, slug, proveedor y categoría son requeridos')
      return
    }

    try {
      const productData = {
        name: formData.name,
        slug: formData.slug,
        presentation: formData.presentation,
        supplier: formData.supplier,
        category: parseInt(formData.category),
      }

      if (editingId) {
        await updateMutation.mutateAsync({
          id: editingId,
          data: productData,
        })
      } else {
        await createMutation.mutateAsync(productData)
      }
      handleCloseForm()
    } catch (err: any) {
      const errorMsg = err.response?.data?.name?.[0] || 
                      err.response?.data?.slug?.[0] ||
                      err.response?.data?.category?.[0] ||
                      err.response?.data?.supplier?.[0] ||
                      err.response?.data?.error ||
                      'Error al guardar el producto'
      setSubmitError(errorMsg)
    }
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este producto?')) {
      try {
        await deleteMutation.mutateAsync(id)
      } catch (err: any) {
        setSubmitError('Error al eliminar el producto')
      }
    }
  }

  return (
    <ProtectedLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Productos</h1>
          <Button onClick={handleOpenForm} variant="primary">
            + Nuevo Producto
          </Button>
        </div>

        {error && (
          <Alert type="error" message="Error al cargar los productos" />
        )}

        {showForm && (
          <Card className="bg-primary-50 border-2 border-primary-200">
            <h2 className="text-xl font-bold mb-4">
              {editingId ? 'Editar' : 'Nuevo'} Producto
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
                placeholder="Ej: Laptop Dell"
                required
                disabled={createMutation.isPending || updateMutation.isPending}
              />

              <Input
                label="Slug"
                name="slug"
                value={formData.slug}
                onChange={handleInputChange}
                placeholder="laptop-dell"
                required
                disabled={createMutation.isPending || updateMutation.isPending}
              />

              <Select
                label="Categoría"
                name="category"
                value={formData.category}
                onChange={handleInputChange}
                options={categoryOptions}
                required
                disabled={createMutation.isPending || updateMutation.isPending}
              />

              <Input
                label="Presentación"
                name="presentation"
                value={formData.presentation}
                onChange={handleInputChange}
                placeholder="Ej: Caja"
                disabled={createMutation.isPending || updateMutation.isPending}
              />

              <Input
                label="Proveedor"
                name="supplier"
                value={formData.supplier}
                onChange={handleInputChange}
                placeholder="Ej: Dell Inc"
                required
                disabled={createMutation.isPending || updateMutation.isPending}
              />

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
        ) : products && products.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-100 border-b">
                <tr>
                  <th className="px-4 py-2 text-left font-medium">Nombre</th>
                  <th className="px-4 py-2 text-left font-medium">Categoría</th>
                  <th className="px-4 py-2 text-left font-medium">Proveedor</th>
                  <th className="px-4 py-2 text-left font-medium">Presentación</th>
                  <th className="px-4 py-2 text-right font-medium">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {products.map((product) => (
                  <tr key={product.id} className="border-b hover:bg-gray-50">
                    <td className="px-4 py-3">{product.name}</td>
                    <td className="px-4 py-3">
                      {typeof product.category === 'number'
                        ? 'Categoría'
                        : product.category.name}
                    </td>
                    <td className="px-4 py-3">{product.supplier}</td>
                    <td className="px-4 py-3">{product.presentation || '-'}</td>
                    <td className="px-4 py-3 text-right space-x-2">
                      <Button 
                        size="sm" 
                        variant="secondary"
                        onClick={() => {
                          setFormData({
                            name: product.name,
                            slug: product.slug,
                            presentation: product.presentation || '',
                            supplier: product.supplier,
                            category: String(product.category),
                          })
                          setEditingId(product.id)
                          setShowForm(true)
                        }}
                      >
                        Editar
                      </Button>
                      <Button 
                        size="sm" 
                        variant="danger"
                        onClick={() => handleDelete(product.id)}
                        isLoading={deleteMutation.isPending}
                      >
                        Eliminar
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <Card className="text-center py-12">
            <p className="text-gray-600">No hay productos registrados</p>
          </Card>
        )}
      </div>
    </ProtectedLayout>
  )
}
