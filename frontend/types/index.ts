// Auth Types
export interface LoginCredentials {
  email: string
  password: string
}

export interface LoginResponse {
  access: string
  refresh: string
  user: User
}

export interface User {
  id: number
  email: string
  username: string
  first_name: string
  last_name: string
  company_id: number
}

export interface RegisterData {
  email: string
  password: string
  password_confirm: string
  first_name: string
  last_name: string
  username: string
  company_name: string
}

// Category Types
export interface Category {
  id: number
  name: string
  description: string
  slug: string
  company: number
  created_at: string
  updated_at: string
}

export interface CategoryCreate {
  name: string
  description?: string
  slug: string
}

// Product Types
export interface Product {
  id: number
  name: string
  slug: string
  presentation?: string
  supplier: string
  category: number | Category
  company: number
  created_at: string
  updated_at: string
}

export interface ProductCreate {
  name: string
  slug: string
  presentation?: string
  supplier: string
  category: number
}

// Batch Types
export interface Batch {
  id: number
  code: string
  product: number | Product
  quantity_received: number
  quantity_available: number
  purchase_price: string
  expiration_date: string
  received_at: string
  supplier: string
}

export interface BatchCreate {
  code: string
  product: number
  quantity_received: number
  quantity_available?: number
  purchase_price: string
  expiration_date?: string | null
  supplier: string
}

// Movement Types
export interface Movement {
  id: number
  product: number | Product
  batch: number | Batch
  batch_code?: string
  quantity: number
  movement_type: 'IN' | 'OUT' | 'ADJUST' | 'EXPIRED'
  reason: string
  created_at: string
  created_by: number | User
}

export interface MovementCreate {
  product?: number
  batch_code?: string
  batch?: number
  quantity: number
  movement_type: 'IN' | 'OUT' | 'ADJUST' | 'EXPIRED'
  reason?: string
}

// API Response Types
export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface ErrorResponse {
  error: string
  detail?: string
  [key: string]: any
}
