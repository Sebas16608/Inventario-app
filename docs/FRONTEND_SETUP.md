# 🚀 Guía de Inicio - Frontend Next.js

## Resumen

He creado un frontend completamente funcional en Next.js 14 con TypeScript para tu aplicación de inventario. Todo está conectado al backend Django que ya tienes.

## 📁 Estructura Creada

```
frontend/
├── app/                      # Páginas (Next.js App Router)
├── components/               # Componentes reutilizables
├── lib/                      # Cliente API y hooks de React Query
├── hooks/                    # Custom hooks
├── types/                    # Tipos TypeScript
├── package.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.ts
└── README.md
```

## 🎯 Pasos para Empezar

### 1️⃣ Instalar Dependencias

```bash
cd frontend
npm install
```

O usar el script automático:

```bash
./setup.sh
```

### 2️⃣ Configurar Variables de Entorno

```bash
cp .env.example .env.local
```

Edita `.env.local` si necesitas cambiar la URL del backend:

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_AUTH_URL=http://localhost:8000/auth
```

### 3️⃣ Iniciar el Servidor de Desarrollo

```bash
npm run dev
```

La app estará disponible en: **http://localhost:3000**

### 4️⃣ Opcionalmente, Ejecutar Todo Junto

Desde la raíz del proyecto:

```bash
./run-dev.sh
```

Esto inicia tanto el backend como el frontend.

## 📋 Características Implementadas

### Autenticación ✅
- Login y registro con JWT
- Token guardado en localStorage
- Redireccionamiento automático si no estás autenticado
- Logout desde la navbar

### Gestión de Categorías ✅
- Listar todas las categorías
- Crear nueva categoría
- Editar categoría existente (interfaz lista, lógica pendiente)
- Eliminar categoría (interfaz lista, lógica pendiente)

### Gestión de Productos ✅
- Listar todos los productos
- Crear nuevo producto (interfaz lista, lógica pendiente)
- Editar producto (interfaz lista, lógica pendiente)
- Eliminar producto (interfaz lista, lógica pendiente)
- Filtrar por categoría

### Movimientos ✅
- Historial de movimientos de inventario
- Mostrar tipo (Entrada/Salida) con colores
- Fechas formateadas

### Dashboard ✅
- Vista general de la aplicación
- Placeholder para estadísticas

### UI/UX ✅
- Diseño responsivo con Tailwind CSS
- Componentes reutilizables (Button, Input, Select, Card, Alert)
- Navbar con navegación
- Alertas para errores
- Loading spinners

## 🔗 Cómo Conecta al Backend

El cliente API está en `lib/api.ts`:

```javascript
import api from '@/lib/api'

// Las llamadas automáticamente:
// 1. PAsasan el token JWT en el header
// 2. Redirigen a /login si el token expira (401)
// 3. Usan la URL base configurada en .env
```

Los hooks de React Query están en `lib/hooks.ts`:

```javascript
import { useCategories, useProducts } from '@/lib/hooks'

// Automáticamente manejan loading, error y caché
```

## 🔧 Próximos Pasos (Funcionalidad Completa)

### Para Luego Completar:

1. **Lógica de Crear/Editar/Eliminar:**
   - Reemplazar botones placeholder con mutaciones reales
   - Agregar validación de formularios
   - Mostrar mensajes de éxito

2. **Dashboard Estadísticas:**
   - Contar productos, categorías, lotes, movimientos
   - Gráficos de movimientos

3. **Gestión de Lotes/Batches:**
   - Página de gestión de lotes
   - Editar cantidad disponible
   - Ver fecha de expiración

4. **Buscar y Filtrar:**
   - Búsqueda por nombre
   - Filtros avanzados
   - Paginación

5. **Mejorar UI:**
   - Agregar más Shadcn UI components
   - Modales para acciones
   - Confirmación antes de eliminar

6. **Reportes:**
   - Exportar a Excel
   - PDF de movimientos
   - Gráficos de stock

## 📱 Páginas Disponibles

| URL | Descripción | Estado |
|-----|-------------|--------|
| `/login` | Iniciar sesión | ✅ Funcional |
| `/register` | Registrarse | ✅ Funcional |
| `/dashboard` | Dashboard principal | ✅ Básico |
| `/categories` | Gestión de categorías | 🟡 UI lista |
| `/products` | Gestión de productos | 🟡 UI lista |
| `/movements` | Historial de movimientos | ✅ Funcional |

✅ = Completamente funcional
🟡 = UI completa, lógica de API pendiente

## 🎨 Stack Tecnológico

- **Next.js 14**: Framework React moderno
- **TypeScript**: Seguridad de tipos
- **Tailwind CSS**: Estilos responsivos
- **React Query**: Manejo de estado y caché de datos
- **Axios**: Cliente HTTP
- **Zustand**: State management (opcional)

## ⚡ Tips Útiles

### Ver la API en la consola del navegador:
```javascript
import api from '@/lib/api'
api.get('/categories/')
```

### Verificar el token:
```javascript
localStorage.getItem('access_token')
localStorage.getItem('user')
```

### Limpiar caché (React Query):
```javascript
import { useQueryClient } from '@tanstack/react-query'
const queryClient = useQueryClient()
queryClient.clear()
```

## 📞 Problemas Comunes

**¿Problema: "Cannot GET /api/categories"?**
- Asegúrate que el backend está corriendo en http://localhost:8000
- Verifica `NEXT_PUBLIC_API_URL` en `.env.local`

**¿Problema: "Token inválido"?**
- Borra localStorage: `localStorage.clear()`
- Vuelve a registrarte/loguearte

**¿Problema: CORS?** (Probablemente sí)
- En tu backend Django, agrega en `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

## 🚀 Deployment

Para producción:

```bash
npm run build
npm run start
```

O usar Vercel (recomendado):

```bash
npm install -g vercel
vercel
```

---

**¿Preguntas o necesitas más funcionalidad?** ¡Avisame!
