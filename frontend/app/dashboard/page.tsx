'use client'

import React from 'react'
import { useProducts, useCategories, useBatches, useMovements } from '@/lib/hooks'
import { ProtectedLayout } from '@/app/layout/ProtectedLayout'
import { Card } from '@/components/Card'
import Link from 'next/link'

export default function DashboardPage() {
  const { data: products, isLoading: productsLoading } = useProducts()
  const { data: categories, isLoading: categoriesLoading } = useCategories()
  const { data: batches, isLoading: batchesLoading } = useBatches()
  const { data: movements, isLoading: movementsLoading } = useMovements()

  const recentMovements = movements?.slice(0, 5) || []
  const totalProducts = products?.length || 0
  const totalCategories = categories?.length || 0
  const totalBatches = batches?.length || 0
  const totalMovements = movements?.length || 0

  const StatCard = ({ title, value, subtitle, link }: { title: string; value: number | string; subtitle: string; link?: string }) => (
    <Link href={link || '#'}>
      <Card className="hover:shadow-lg transition-shadow cursor-pointer">
        <h3 className="text-sm font-medium text-gray-600">{title}</h3>
        <p className="text-3xl font-bold mt-2">{value}</p>
        <p className="text-xs text-gray-500 mt-2">{subtitle}</p>
      </Card>
    </Link>
  )

  return (
    <ProtectedLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-gray-600 mt-2">Bienvenido a tu panel de control</p>
        </div>

        {/* Tarjetas de resumen */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard
            title="Productos"
            value={productsLoading ? '--' : totalProducts}
            subtitle="productos registrados"
            link="/products"
          />
          <StatCard
            title="Categorías"
            value={categoriesLoading ? '--' : totalCategories}
            subtitle="categorías activas"
            link="/categories"
          />
          <StatCard
            title="Lotes"
            value={batchesLoading ? '--' : totalBatches}
            subtitle="lotes en inventario"
            link="/batches"
          />
          <StatCard
            title="Movimientos"
            value={movementsLoading ? '--' : totalMovements}
            subtitle="movimientos registrados"
            link="/movements"
          />
        </div>

        {/* Últimas actividades */}
        <Card>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold">Últimos Movimientos</h2>
            <Link href="/movements">
              <p className="text-sm text-blue-600 hover:text-blue-800">Ver todos</p>
            </Link>
          </div>

          {movementsLoading ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            </div>
          ) : recentMovements.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="border-b">
                  <tr>
                    <th className="text-left py-2">Producto</th>
                    <th className="text-center">Cantidad</th>
                    <th className="text-left">Tipo</th>
                    <th className="text-left">Fecha</th>
                  </tr>
                </thead>
                <tbody>
                  {recentMovements.map((movement: any) => (
                    <tr key={movement.id} className="border-b hover:bg-gray-50">
                      <td className="py-2">
                        {typeof movement.product === 'number'
                          ? 'Producto'
                          : movement.product.name}
                      </td>
                      <td className="text-center">{movement.quantity}</td>
                      <td>
                        <span
                          className={`px-2 py-1 rounded text-xs font-semibold ${
                            movement.movement_type === 'IN'
                              ? 'bg-green-100 text-green-800'
                              : 'bg-red-100 text-red-800'
                          }`}
                        >
                          {movement.movement_type}
                        </span>
                      </td>
                      <td className="text-gray-600 text-xs">
                        {new Date(movement.created_at).toLocaleDateString('es-ES')}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-gray-600 py-8 text-center">No hay movimientos registrados aún</p>
          )}
        </Card>

        {/* Acceso rápido */}
        <Card>
          <h2 className="text-xl font-bold mb-4">Acceso Rápido</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Link href="/categories">
              <button className="w-full p-4 border-2 border-gray-200 rounded hover:border-blue-500 hover:bg-blue-50 transition">
                <p className="text-sm font-semibold">➕ Nueva Categoría</p>
              </button>
            </Link>
            <Link href="/products">
              <button className="w-full p-4 border-2 border-gray-200 rounded hover:border-blue-500 hover:bg-blue-50 transition">
                <p className="text-sm font-semibold">📦 Nuevo Producto</p>
              </button>
            </Link>
            <Link href="/batches">
              <button className="w-full p-4 border-2 border-gray-200 rounded hover:border-blue-500 hover:bg-blue-50 transition">
                <p className="text-sm font-semibold">📋 Nuevo Lote</p>
              </button>
            </Link>
            <Link href="/movements">
              <button className="w-full p-4 border-2 border-gray-200 rounded hover:border-blue-500 hover:bg-blue-50 transition">
                <p className="text-sm font-semibold">🔄 Movimiento</p>
              </button>
            </Link>
          </div>
        </Card>
      </div>
    </ProtectedLayout>
  )
}
