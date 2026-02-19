'use client'

import React from 'react'
import { ProtectedLayout } from '@/app/layout/ProtectedLayout'
import { Card } from '@/components/Card'

export default function DashboardPage() {
  return (
    <ProtectedLayout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold">Dashboard</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <h3 className="text-sm font-medium text-gray-600">Productos</h3>
            <p className="text-3xl font-bold mt-2">--</p>
            <p className="text-xs text-gray-500 mt-2">Total registrados</p>
          </Card>

          <Card>
            <h3 className="text-sm font-medium text-gray-600">Categorías</h3>
            <p className="text-3xl font-bold mt-2">--</p>
            <p className="text-xs text-gray-500 mt-2">Total registradas</p>
          </Card>

          <Card>
            <h3 className="text-sm font-medium text-gray-600">Lotes</h3>
            <p className="text-3xl font-bold mt-2">--</p>
            <p className="text-xs text-gray-500 mt-2">Total disponibles</p>
          </Card>

          <Card>
            <h3 className="text-sm font-medium text-gray-600">Movimientos</h3>
            <p className="text-3xl font-bold mt-2">--</p>
            <p className="text-xs text-gray-500 mt-2">Total este mes</p>
          </Card>
        </div>

        <Card>
          <h2 className="text-xl font-bold mb-4">Últimas Actividades</h2>
          <div className="space-y-2">
            <p className="text-gray-600">No hay movimientos registrados</p>
          </div>
        </Card>
      </div>
    </ProtectedLayout>
  )
}
