'use client'

import React from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

export function Navbar() {
  const router = useRouter()

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    router.push('/login')
  }

  return (
    <nav className="bg-primary-600 text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link href="/dashboard" className="text-2xl font-bold">
            Invorax
          </Link>
          <ul className="flex gap-6">
            <li>
              <Link href="/dashboard" className="hover:opacity-80 transition">
                Dashboard
              </Link>
            </li>
            <li>
              <Link href="/categories" className="hover:opacity-80 transition">
                Categorías
              </Link>
            </li>
            <li>
              <Link href="/products" className="hover:opacity-80 transition">
                Productos
              </Link>
            </li>
            <li>
              <Link href="/batches" className="hover:opacity-80 transition">
                Lotes
              </Link>
            </li>
            <li>
              <Link href="/movements" className="hover:opacity-80 transition">
                Movimientos
              </Link>
            </li>
            <li>
              <button
                onClick={handleLogout}
                className="hover:opacity-80 transition"
              >
                Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  )
}
