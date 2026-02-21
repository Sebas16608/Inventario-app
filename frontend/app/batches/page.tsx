'use client'

import React, { useState } from 'react'
import { useBatches, useProducts, useCreateBatch, useUpdateBatch, useDeleteBatch } from '@/lib/hooks'
import { ProtectedLayout } from '@/app/layout/ProtectedLayout'
import { Card } from '@/components/Card'
import { Button } from '@/components/Button'
import { Input } from '@/components/Input'
import { Select } from '@/components/Select'
import { Alert } from '@/components/Alert'

export default function BatchesPage() {
  const { data: batches, isLoading, error } = useBatches()
  const { data: products } = useProducts()
  const createMutation = useCreateBatch()
  const updateMutation = useUpdateBatch()
  const deleteMutation = useDeleteBatch()
  
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [formData, setFormData] = useState({
    product: '',
    quantity_received: '',
    quantity_available: '',
    purchase_price: '',
    expiration_date: '',
    supplier: '',
  })
  const [submitError, setSubmitError] = useState('')

  const productOptions = (products || []).map((prod) => ({
    value: String(prod.id),
    label: `${prod.name} (${prod.supplier})`,
  }))

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleOpenForm = () => {
    setFormData({
      product: '',
      quantity_received: '',
      quantity_available: '',
      purchase_price: '',
      expiration_date: '',
      supplier: '',
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

    if (!formData.product || !formData.quantity_received || !formData.purchase_price || !formData.supplier) {
      setSubmitError('Producto, cantidad, precio y proveedor son requeridos')
      return
    }

    try {
      const batchData = {
        product: parseInt(formData.product),
        quantity_received: parseInt(formData.quantity_received),
        quantity_available: formData.quantity_available 
          ? parseInt(formData.quantity_available) 
          : parseInt(formData.quantity_received),
        purchase_price: formData.purchase_price,
        expiration_date: formData.expiration_date || null,
        supplier: formData.supplier,
      }

      if (editingId) {
        await updateMutation.mutateAsync({
          id: editingId,
          data: batchData,
        })
      } else {
        await createMutation.mutateAsync(batchData)
      }
      handleCloseForm()
    } catch (err: any) {
      const errorMsg = err.response?.data?.product?.[0] || 
                      err.response?.data?.error ||
                      'Error al guardar el lote'
      setSubmitError(errorMsg)
    }
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este lote?')) {
      try {
        await deleteMutation.mutateAsync(id)
      } catch (err: any) {
        setSubmitError('Error al eliminar el lote')
      }
    }
  }

  return (
    <ProtectedLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Lotes</h1>
          <Button onClick={handleOpenForm} variant="primary">
            + Nuevo Lote
          </Button>
        </div>

        {error && (
          <Alert type="error" message="Error al cargar los lotes" />
        )}

        {showForm && (
          <Card className="bg-primary-50 border-2 border-primary-200">
            <h2 className="text-xl font-bold mb-4">
              {editingId ? 'Editar' : 'Nuevo'} Lote
            </h2>
            {submitError && (
              <Alert type="error" message={submitError} onClose={() => setSubmitError('')} />
            )}
            <form className="space-y-4" onSubmit={handleSubmit}>
              <Select
                label="Producto"
                name="product"
                value={formData.product}
                onChange={handleInputChange}
                options={productOptions}
                required
                disabled={createMutation.isPending || updateMutation.isPending}
              />

              <Input
                label="Cantidad Recibida"
                type="number"
                name="quantity_received"
                value={formData.quantity_received}
                onChange={handleInputChange}
                placeholder="100"
                required
                min="1"
                disabled={createMutation.isPending || updateMutation.isPending}
              />

              <Input
                label="Cantidad Disponible"
                type="number"
                name="quantity_available"
                value={formData.quantity_available}
                onChange={handleInputChange}
                placeholder="100 (por defecto igual a recibida)"
                min="0"
                disabled={createMutation.isPending || updateMutation.isPending}
              />

              <Input
                label="Precio de Compra"
                type="number"
                step="0.01"
                name="purchase_price"
                value={formData.purchase_price}
                onChange={handleInputChange}
                placeholder="10.50"
                required
                disabled={createMutation.isPending || updateMutation.isPending}
              />

              <Input
                label="Fecha de Vencimiento"
                type="date"
                name="expiration_date"
                value={formData.expiration_date}
                onChange={handleInputChange}
                disabled={createMutation.isPending || updateMutation.isPending}
              />

              <Input
                label="Proveedor"
                name="supplier"
                value={formData.supplier}
                onChange={handleInputChange}
                placeholder="Nombre del proveedor"
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
        ) : batches && batches.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-100 border-b">
                <tr>
                  <th className="px-4 py-2 text-left font-medium">Código</th>
                  <th className="px-4 py-2 text-left font-medium">Producto</th>
                  <th className="px-4 py-2 text-center font-medium">Recibida</th>
                  <th className="px-4 py-2 text-center font-medium">Disponible</th>
                  <th className="px-4 py-2 text-right font-medium">Precio</th>
                  <th className="px-4 py-2 text-left font-medium">Vencimiento</th>
                  <th className="px-4 py-2 text-left font-medium">Proveedor</th>
                  <th className="px-4 py-2 text-right font-medium">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {batches.map((batch) => {
                  const productId = typeof batch.product === 'number' ? batch.product : batch.product.id
                  const productName = products?.find(p => p.id === productId)?.name || 'Producto no encontrado'
                  return (
                  <tr key={batch.id} className="border-b hover:bg-gray-50">
                    <td className="px-4 py-3 font-mono text-sm">{batch.code}</td>
                    <td className="px-4 py-3">
                      {productName}
                    </td>
                    <td className="px-4 py-3 text-center">{batch.quantity_received}</td>
                    <td className="px-4 py-3 text-center">{batch.quantity_available}</td>
                    <td className="px-4 py-3 text-right">Q{batch.purchase_price}</td>
                    <td className="px-4 py-3">
                      {new Date(batch.expiration_date).toLocaleDateString('es-ES')}
                    </td>
                    <td className="px-4 py-3">{batch.supplier}</td>
                    <td className="px-4 py-3 text-right space-x-2">
                      <Button 
                        size="sm" 
                        variant="secondary"
                        onClick={() => {
                          setFormData({
                            product: String(typeof batch.product === 'number' ? batch.product : batch.product.id),
                            quantity_received: String(batch.quantity_received),
                            quantity_available: String(batch.quantity_available),
                            purchase_price: batch.purchase_price,
                            expiration_date: batch.expiration_date || '',
                            supplier: batch.supplier,
                          })
                          setEditingId(batch.id)
                          setShowForm(true)
                        }}
                      >
                        Editar
                      </Button>
                      <Button 
                        size="sm" 
                        variant="danger"
                        onClick={() => handleDelete(batch.id)}
                        isLoading={deleteMutation.isPending}
                      >
                        Eliminar
                      </Button>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <Card className="text-center py-12">
            <p className="text-gray-600">No hay lotes registrados</p>
          </Card>
        )}
      </div>
    </ProtectedLayout>
  )
}
