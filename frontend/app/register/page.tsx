'use client'

import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Input } from '@/components/Input'
import { Button } from '@/components/Button'
import { Card } from '@/components/Card'
import { Alert } from '@/components/Alert'
import api, { authAPI } from '@/lib/api'
import { LoginResponse } from '@/types'

export default function RegisterPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    first_name: '',
    last_name: '',
    password: '',
    password_confirm: '',
    company_name: '',
  })
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      router.push('/dashboard')
    }
  }, [router])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (formData.password !== formData.password_confirm) {
      setError('Las contraseñas no coinciden')
      return
    }

    if (!formData.company_name.trim()) {
      setError('El nombre de la empresa es requerido')
      return
    }

    setIsLoading(true)

    try {
      const response = await authAPI.post<LoginResponse>('/register/', {
        email: formData.email,
        username: formData.username,
        first_name: formData.first_name,
        last_name: formData.last_name,
        password: formData.password,
        company_name: formData.company_name,
      })

      const { access, user } = response.data
      localStorage.setItem('access_token', access)
      localStorage.setItem('user', JSON.stringify(user))
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`

      router.push('/dashboard')
    } catch (err: any) {
      // Intentar obtener el error de diferentes formas
      let errorMsg = 'Error al registrarse'
      
      if (err.response?.data?.error) {
        errorMsg = err.response.data.error
      } else if (err.response?.data?.detail) {
        errorMsg = err.response.data.detail
      } else if (typeof err.response?.data === 'string') {
        errorMsg = err.response.data
      } else if (err.response?.status === 400) {
        // Si es 400, mostrar los errores del serializer
        const errors = err.response?.data
        if (typeof errors === 'object') {
          const errorMessages = Object.entries(errors).map(([field, messages]) => {
            if (Array.isArray(messages)) {
              return `${field}: ${messages.join(', ')}`
            }
            return `${field}: ${messages}`
          })
          errorMsg = errorMessages.join(' | ')
        }
      }
      
      setError(errorMsg)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-8">Crear Cuenta</h1>

        {error && (
          <Alert
            type="error"
            message={error}
            onClose={() => setError('')}
          />
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Email"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="tu@email.com"
            required
            disabled={isLoading}
          />

          <Input
            label="Usuario"
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            placeholder="usuario"
            required
            disabled={isLoading}
          />

          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Nombre"
              type="text"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
              placeholder="Juan"
              required
              disabled={isLoading}
            />
            <Input
              label="Apellido"
              type="text"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
              placeholder="Pérez"
              required
              disabled={isLoading}
            />
          </div>

          <Input
            label="Empresa"
            type="text"
            name="company_name"
            value={formData.company_name}
            onChange={handleChange}
            placeholder="Mi Empresa"
            required
            disabled={isLoading}
          />

          <Input
            label="Contraseña"
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="••••••••"
            required
            disabled={isLoading}
          />

          <Input
            label="Confirmar Contraseña"
            type="password"
            name="password_confirm"
            value={formData.password_confirm}
            onChange={handleChange}
            placeholder="••••••••"
            required
            disabled={isLoading}
          />

          <Button
            type="submit"
            isLoading={isLoading}
            className="w-full"
          >
            Registrarse
          </Button>
        </form>

        <p className="text-center mt-6 text-gray-600">
          ¿Ya tienes cuenta?{' '}
          <Link href="/login" className="text-primary-600 font-medium hover:underline">
            Inicia Sesión
          </Link>
        </p>
      </Card>
    </div>
  )
}
