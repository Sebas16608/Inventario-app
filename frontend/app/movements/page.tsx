'use client'

import React, { useState } from 'react'
import { useMovements, useBatches, useCreateMovement, useUpdateMovement, useDeleteMovement } from '@/lib/hooks'
import { ProtectedLayout } from '@/app/layout/ProtectedLayout'
import { Card } from '@/components/Card'
import { Button } from '@/components/Button'
import { Input } from '@/components/Input'
import { Select } from '@/components/Select'
import { Alert } from '@/components/Alert'

export default function MovementsPage() {
  const { data: movements, isLoading, error } = useMovements()
  const { data: batches } = useBatches()
  const createMutation = useCreateMovement()
  const updateMutation = useUpdateMovement()
  const deleteMutation = useDeleteMovement()
  
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [formData, setFormData] = useState({
    batch: '',
    quantity: '',
    movement_type: 'IN',
    reason: '',
  })
  const [submitError, setSubmitError] = useState('')

  const batchOptions = (batches || []).map((batch) => ({
    value: batch.code || String(batch.id),
    label: `Lote ${batch.code || batch.id} - ${typeof batch.product === 'number' ? 'Producto' : batch.product.name}`,
  }))

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleOpenForm = () => {
    setFormData({
      batch: '',
      quantity: '',
      movement_type: 'IN',
      reason: '',
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

    if (!formData.batch || !formData.quantity) {
      setSubmitError('Lote y cantidad son requeridos')
      return
    }

    try {
      const selectedBatch = batches?.find(b => (b.code || String(b.id)) === formData.batch)
      if (!selectedBatch) {
        setSubmitError('Lote no encontrado')
        return
      }

      const movementData = {
        batch_code: selectedBatch.code || undefined,
        quantity: parseInt(formData.quantity),
        movement_type: formData.movement_type as 'IN' | 'OUT' | 'ADJUST' | 'EXPIRED',
        reason: formData.reason,
      }

      if (editingId) {
        await updateMutation.mutateAsync({
          id: editingId,
          data: movementData,
        })
      } else {
        await createMutation.mutateAsync(movementData)
      }
      handleCloseForm()
    } catch (err: any) {
      const errorMsg = err.response?.data?.batch?.[0] || 
                      err.response?.data?.error ||
                      'Error al guardar el movimiento'
      setSubmitError(errorMsg)
    }
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este movimiento?')) {
      try {
        await deleteMutation.mutateAsync(id)
      } catch (err: any) {
        setSubmitError('Error al eliminar el movimiento')
      }
    }
  }

  return (
    <ProtectedLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Movimientos de Inventario</h1>
          <Button onClick={handleOpenForm} variant="primary">
            + Nuevo Movimiento
          </Button>
        </div>

        {error && (
          <Alert type="error" message="Error al cargar los movimientos" />
        )}

        {showForm && (
          <Card className="bg-primary-50 border-2 border-primary-200">
            <h2 className="text-xl font-bold mb-4">
              {editingId ? 'Editar' : 'Nuevo'} Movimiento
            </h2>
            {submitError && (
              <Alert type="error" message={submitError} onClose={() => setSubmitError('')} />
            )}
            <form className="space-y-4" onSubmit={handleSubmit}>
              <Select
                label="Lote"
                name="batch"
                value={formData.batch}
                onChange={handleInputChange}
                options={batchOptions}
                required
                disabled={createMutation.isPending || updateMutation.isPending}
              />

              <Select
                label="Tipo de Movimiento"
                name="movement_type"
                value={formData.movement_type}
                onChange={handleInputChange}
                options={[
                  { value: 'IN', label: 'Entrada (IN)' },
                  { value: 'OUT', label: 'Salida (OUT)' },
                  { value: 'ADJUST', label: 'Ajuste (ADJUST)' },
                  { value: 'EXPIRED', label: 'Vencido (EXPIRED)' },
                ]}
                required
                disabled={createMutation.isPending || updateMutation.isPending}
              />

              <Input
                label="Cantidad"
                type="number"
                name="quantity"
                value={formData.quantity}
                onChange={handleInputChange}
                placeholder="10"
                required
                min="1"
                disabled={createMutation.isPending || updateMutation.isPending}
              />

              <Input
                label="Razón / Observaciones"
                name="reason"
                value={formData.reason}
                onChange={handleInputChange}
                placeholder="Venta, devolución, merma, etc."
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
        ) : movements && movements.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-100 border-b">
                <tr>
                  <th className="px-4 py-2 text-left font-medium">Producto</th>
                  <th className="px-4 py-2 text-center font-medium">Lote</th>
                  <th className="px-4 py-2 text-center font-medium">Cantidad</th>
                  <th className="px-4 py-2 text-left font-medium">Tipo</th>
                  <th className="px-4 py-2 text-left font-medium">Razón</th>
                  <th className="px-4 py-2 text-left font-medium">Fecha</th>
                  <th className="px-4 py-2 text-right font-medium">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {movements.map((movement: any) => (
                  <tr key={movement.id} className="border-b hover:bg-gray-50">
                    <td className="px-4 py-3">
                      {typeof movement.product === 'number' ? 'Producto' : movement.product.name}
                    </td>
                    <td className="px-4 py-3 text-center">
                      {typeof movement.batch === 'number' 
                        ? movement.batch 
                        : (movement as any).batch_code || movement.batch.id}
                    </td>
                    <td className="px-4 py-3 text-center">{movement.quantity}</td>
                    <td className="px-4 py-3">
                      <span
                        className={`px-3 py-1 rounded text-sm font-semibold ${
                          movement.movement_type === 'IN'
                            ? 'bg-green-200 text-green-800'
                            : 'bg-red-200 text-red-800'
                        }`}
                      >
                        {movement.movement_type}
                      </span>
                    </td>
                    <td className="px-4 py-3">{movement.reason}</td>
                    <td className="px-4 py-3">
                      {new Date(movement.created_at).toLocaleDateString('es-ES')}
                    </td>
                    <td className="px-4 py-3 text-right space-x-2">
                      <Button 
                        size="sm" 
                        variant="secondary"
                        onClick={() => {
                          const batchCode = (movement as any).batch_code 
                            || (typeof movement.batch === 'number' ? String(movement.batch) : movement.batch.id)
                          setFormData({
                            batch: batchCode,
                            quantity: String(movement.quantity),
                            movement_type: movement.movement_type,
                            reason: movement.reason,
                          })
                          setEditingId(movement.id)
                          setShowForm(true)
                        }}
                      >
                        Editar
                      </Button>
                      <Button 
                        size="sm" 
                        variant="danger"
                        onClick={() => handleDelete(movement.id)}
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
            <p className="text-gray-600">No hay movimientos registrados</p>
          </Card>
        )}
      </div>
    </ProtectedLayout>
  )
}
