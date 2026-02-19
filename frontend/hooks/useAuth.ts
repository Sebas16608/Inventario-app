import { useState, useCallback, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import api, { authAPI } from '@/lib/api'
import { LoginCredentials, LoginResponse, RegisterData, User } from '@/types'

interface AuthState {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  isLoading: boolean
  error: string | null
  isAuthenticated: boolean
}

const TOKEN_EXPIRY_TIME = 3600 * 1000 // 1 hora en ms

export function useAuth() {
  const router = useRouter()
  const [state, setState] = useState<AuthState>({
    user: null,
    accessToken: null,
    refreshToken: null,
    isLoading: false,
    error: null,
    isAuthenticated: false,
  })

  // Initialize from localStorage
  useEffect(() => {
    const accessToken = localStorage.getItem('access_token')
    const refreshToken = localStorage.getItem('refresh_token')
    const userJson = localStorage.getItem('user')

    if (accessToken && userJson) {
      try {
        const user = JSON.parse(userJson)
        setState((prev: AuthState) => ({
          ...prev,
          accessToken,
          refreshToken,
          user,
          isAuthenticated: true,
        }))
        // Set auth header
        api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
      } catch (e) {
        // Clear corrupted data
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
      }
    }
  }, [])

  const refreshAccessToken = useCallback(async () => {
    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) {
      setState((prev: AuthState) => ({
        ...prev,
        isAuthenticated: false,
        accessToken: null,
      }))
      return false
    }

    try {
      const response = await authAPI.post<{ access: string }>('/token/refresh/', {
        refresh: refreshToken,
      })
      const { access } = response.data

      localStorage.setItem('access_token', access)
      setState((prev: AuthState) => ({
        ...prev,
        accessToken: access,
      }))
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`
      return true
    } catch (error) {
      // Refresh token invalid or expired
      logout()
      return false
    }
  }, [])

  const login = useCallback(
    async (credentials: LoginCredentials) => {
      setState((prev: AuthState) => ({ ...prev, isLoading: true, error: null }))
      try {
        const response = await authAPI.post<LoginResponse>('/login/', credentials)
        const { access, refresh, user } = response.data

        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
        localStorage.setItem('user', JSON.stringify(user))
        api.defaults.headers.common['Authorization'] = `Bearer ${access}`

        setState((prev: AuthState) => ({
          ...prev,
          accessToken: access,
          refreshToken: refresh,
          user,
          isLoading: false,
          isAuthenticated: true,
          error: null,
        }))

        router.push('/dashboard')
      } catch (error: any) {
        const errorMsg =
          error.response?.data?.detail ||
          error.response?.data?.error ||
          'Error al iniciar sesión'
        setState((prev: AuthState) => ({
          ...prev,
          error: errorMsg,
          isLoading: false,
        }))
        throw error
      }
    },
    [router]
  )

  const register = useCallback(
    async (data: RegisterData) => {
      setState((prev: AuthState) => ({ ...prev, isLoading: true, error: null }))
      try {
        const response = await authAPI.post<LoginResponse>('/register/', data)
        const { access, refresh, user } = response.data

        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
        localStorage.setItem('user', JSON.stringify(user))
        api.defaults.headers.common['Authorization'] = `Bearer ${access}`

        setState((prev: AuthState) => ({
          ...prev,
          accessToken: access,
          refreshToken: refresh,
          user,
          isLoading: false,
          isAuthenticated: true,
          error: null,
        }))

        router.push('/dashboard')
      } catch (error: any) {
        const errorMsg =
          error.response?.data?.detail ||
          error.response?.data?.error ||
          'Error al registrarse'
        setState((prev: AuthState) => ({
          ...prev,
          error: errorMsg,
          isLoading: false,
        }))
        throw error
      }
    },
    [router]
  )

  const logout = useCallback(() => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    delete api.defaults.headers.common['Authorization']
    setState({
      user: null,
      accessToken: null,
      refreshToken: null,
      isLoading: false,
      error: null,
      isAuthenticated: false,
    })
    router.push('/login')
  }, [router])

  const clearError = useCallback(() => {
    setState((prev: AuthState) => ({
      ...prev,
      error: null,
    }))
  }, [])

  return {
    ...state,
    login,
    register,
    logout,
    refreshAccessToken,
    clearError,
  }
}
