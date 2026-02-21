'use client'

import React from 'react'
import { useBatches, useProducts } from '@/lib/hooks'
import { ProtectedLayout } from '@/app/layout/ProtectedLayout'
import { Card } from '@/components/Card'

interface StockItem {
  productId: number
  productName: string
  totalReceived: number
  totalAvailable: number
  totalSold: number
  batches: {
    code: string
    quantityAvailable: number
    expirationDate: string
  }[]
}

export default function StockPage() {
  const { data: batches, isLoading: loadingBatches } = useBatches()
  const { data: products, isLoading: loadingProducts } = useProducts()

  const stockByProduct: Record<number, StockItem> = {}

  if (batches && products) {
    batches.forEach((batch) => {
      const productId = typeof batch.product === 'number' ? batch.product : batch.product.id
      const product = products.find(p => p.id === productId)
      
      if (!stockByProduct[productId]) {
        stockByProduct[productId] = {
          productId,
          productName: product?.name || 'Producto no encontrado',
          totalReceived: 0,
          totalAvailable: 0,
          totalSold: 0,
          batches: [],
        }
      }

      stockByProduct[productId].totalReceived += batch.quantity_received
      stockByProduct[productId].totalAvailable += batch.quantity_available
      stockByProduct[productId].totalSold += batch.quantity_received - batch.quantity_available
      stockByProduct[productId].batches.push({
        code: batch.code,
        quantityAvailable: batch.quantity_available,
        expirationDate: batch.expiration_date,
      })
    })
  }

  const stockList = Object.values(stockByProduct)

  const isLoading = loadingBatches || loadingProducts

  return (
    <ProtectedLayout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold">Control de Stock</h1>

        {isLoading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : stockList.length > 0 ? (
          <div className="grid gap-6">
            {stockList.map((item) => (
              <Card key={item.productId}>
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h2 className="text-xl font-bold">{item.productName}</h2>
                    <p className="text-sm text-gray-500">ID: {item.productId}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-green-600">
                      {item.totalAvailable}
                    </div>
                    <div className="text-sm text-gray-500">disponibles</div>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4 mb-4 text-center">
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="text-lg font-semibold">{item.totalReceived}</div>
                    <div className="text-xs text-gray-500">Recibido</div>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="text-lg font-semibold text-red-600">{item.totalSold}</div>
                    <div className="text-xs text-gray-500">Vendido</div>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="text-lg font-semibold text-green-600">{item.totalAvailable}</div>
                    <div className="text-xs text-gray-500">Disponible</div>
                  </div>
                </div>

                {item.batches.length > 0 && (
                  <div className="border-t pt-4">
                    <h3 className="text-sm font-medium text-gray-500 mb-2">Detalle por Lote</h3>
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm">
                        <thead className="bg-gray-50">
                          <tr>
                            <th className="px-3 py-2 text-left font-medium">Lote</th>
                            <th className="px-3 py-2 text-center font-medium">Cantidad</th>
                            <th className="px-3 py-2 text-left font-medium">Vencimiento</th>
                          </tr>
                        </thead>
                        <tbody>
                          {item.batches.map((batch, idx) => (
                            <tr key={idx} className="border-t">
                              <td className="px-3 py-2 font-mono">{batch.code}</td>
                              <td className="px-3 py-2 text-center">{batch.quantityAvailable}</td>
                              <td className="px-3 py-2">
                                {batch.expirationDate 
                                  ? new Date(batch.expirationDate).toLocaleDateString('es-ES')
                                  : '-'}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </Card>
            ))}
          </div>
        ) : (
          <Card className="text-center py-12">
            <p className="text-gray-600">No hay stock disponible</p>
          </Card>
        )}
      </div>
    </ProtectedLayout>
  )
}
