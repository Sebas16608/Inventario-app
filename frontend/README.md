# Frontend - Sistema de Gestión de Inventario

Interfaz web moderna construida con Next.js 14 para gestión de inventarios.

## 🚀 Características

- **Next.js 14** - App Router, Server Components
- **React 18** con TypeScript
- **Tailwind CSS** - Estilos responsive
- **React Query** (@tanstack) - Estado de servidor
- **JWT autenticación** - Tokens seguros
- **Multi-empresa** - Aislamiento de datos
- **CRUD completo** - Categorías, Productos, Lotes, Movimientos

## 🛠️ Requisitos

- Node.js 18+
- npm o yarn

## 📦 Instalación Rápida

```bash
# 1. Instalar dependencias
npm install

# 2. Variables de entorno
cp .env.example .env.local

# 3. Servidor de desarrollo
npm run dev
```

Abre `http://localhost:3000` en tu navegador.

## 🌍 Variables de Entorno

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_AUTH_URL=http://localhost:8000/auth
```

## 📂 Estructura

```
frontend/
├── app/               # Páginas Next.js (App Router)
│   ├── login/         # Autenticación
│   ├── register/      # Registro de usuario
│   ├── dashboard/     # Página principal
│   ├── categories/    # Gestión de categorías
│   ├── products/      # Gestión de productos
│   ├── batches/       # Gestión de lotes
│   ├── movements/     # Historial de movimientos
│   ├── layout/        # Layouts compartidos
│   ├── globals.css    # Estilos globales
│   ├── layout.tsx     # Root layout
│   └── page.tsx       # Home
├── components/        # Componentes reutilizables
│   ├── Navbar.tsx     # Navegación
│   ├── Button.tsx     # Botones
│   ├── Input.tsx      # Campos de entrada
│   ├── Select.tsx     # Select/Dropdown
│   ├── Card.tsx       # Contenedores
│   └── Alert.tsx      # Notificaciones
├── lib/               # Utilidades
│   ├── api.ts         # Configuración Axios
│   └── hooks.ts       # React Query hooks
├── types/             # Tipos TypeScript
│   └── index.ts       # Interfaces
├── hooks/             # React hooks custom
├── public/            # Archivos estáticos
├── next.config.js     # Configuración Next.js
├── tailwind.config.ts # Configuración Tailwind
└── tsconfig.json      # Configuración TypeScript
```

## 🎯 Páginas Principales

### Login (`/login`)
- Email/Usuario + Contraseña
- Guardado de tokens en localStorage
- Redirección a dashboard

### Registro (`/register`)
- Crear usuario nuevo
- Crear empresa nueva
- Email + Contraseña + Nombre empresa

### Dashboard (`/dashboard`)
- Resumen de inventario
- Acceso a módulos

### Categorías (`/categories`)
- Listar categorías
- Crear, editar, eliminar
- Búsqueda y filtrado

### Productos (`/products`)
- Listar productos
- CRUD completo
- Selección de categoría
- Stock y precios

### Lotes (`/batches`)
- Historial de lotes
- Crear lote para producto
- Cantidad recibida vs disponible
- Fecha de vencimiento

### Movimientos (`/movements`)
- Historial de movimientos IN/OUT
- Crear movimiento
- Rastreo por lote
- Razón del movimiento

## 💻 Comandos Disponibles

```bash
# Desarrollo
npm run dev         # Iniciar servidor dev

# Producción
npm run build       # Compilar para producción
npm start           # Iniciar servidor prod

# Otros
npm run lint        # Linting
npm run type-check  # Verificar tipos
```

## 🔐 Autenticación

**Flujo:**
1. Usuario se registra en `/register`
2. Sistema crea empresa automáticamente
3. Login en `/register` con credenciales
4. Tokens JWT guardados en localStorage
5. Interceptor en `lib/api.ts` añade token a peticiones
6. Auto-refresh de token en caso de expiración

**Headers:**
```javascript
Authorization: Bearer <access_token>
```

## 📡 API Integration

Axiós con interceptores para:
- ✅ Agregar token automáticamente
- ✅ Refrescar token si expira
- ✅ Logout si refresh falla
- ✅ Manejo de errores centralizado

Dos instancias:
```typescript
api       // Para /api/* endpoints
authAPI   // Para /auth/* endpoints (login, register)
```

## 🎨 Componentes

### Button
```tsx
<Button variant="primary" size="sm" isLoading={false}>
  Click me
</Button>
```

### Input
```tsx
<Input 
  label="Email"
  type="email"
  value={value}
  onChange={handleChange}
/>
```

### Select
```tsx
<Select
  label="Categoría"
  options={[{ value: '1', label: 'Cat 1' }]}
  value={selected}
  onChange={handleChange}
/>
```

## 🪝 Hooks de React Query

```typescript
// Leer datos
const { data, isLoading, error } = useCategories()
const { data: batch } = useBatch(id)

// Crear/Actualizar/Eliminar
const createMutation = useCreateCategory()
const updateMutation = useUpdateCategory()
const deleteMutation = useDeleteCategory()

// Uso
await createMutation.mutateAsync({ name: 'Nueva' })
```

## 🧪 Testing

```bash
npm run test        # Tests unitarios
npm run test:watch  # Watch mode
```

## 🚢 Build & Deploy

### Local
```bash
npm run build
npm start
```

### Docker
```bash
docker build -t inventario-frontend .
docker run -p 3000:3000 inventario-frontend
```

### Vercel
```bash
# Push a GitHub
# Conectar en Vercel
# Auto-deploy en cada push
```

## 🔒 Seguridad

✅ Tokens almacenados en localStorage  
✅ Auto-logout en error de refresh  
✅ Validación de entrada en forms  
✅ CSRF protection (Next.js)  
✅ Protección de rutas (ProtectedLayout)  

## 📦 Dependencias Principales

```json
{
  "next": "^14.2.35",
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "@tanstack/react-query": "^5.28.0",
  "axios": "^1.6.2",
  "typescript": "^5.3.3",
  "tailwindcss": "^3.3.6"
}
```

## 🐛 Troubleshooting

### Error de CORS
```
Verificar CORS_ALLOWED_ORIGINS en backend/.env
Debe incluir http://localhost:3000
```

### Token expirado
```
Limpiar localStorage y login nuevamente
O esperar auto-refresh
```

### Build falla
```bash
# Limpiar caché
rm -rf .next
npm run build
```

### Puerto 3000 ocupado
```bash
npm run dev -- -p 3001
```

## 📚 Documentación

- `/docs/FRONTEND_SETUP.md` - Setup detallado
- `/docs/FRONTEND_CRUD_GUIDE.md` - Guía CRUD
- `/docs/FRONTEND_SUMMARY.md` - Resumen features
- `/docs/API.md` - Documentación API

## 📞 Contacto

Para bugs o sugerencias, crear un issue en el repositorio.
│   ├── login/                # Página de login
│   ├── register/             # Página de registro
│   └── layout/               # Layouts compartidos
├── components/               # Componentes reutilizables
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Select.tsx
│   ├── Card.tsx
│   ├── Alert.tsx
│   └── Navbar.tsx
├── lib/                      # Librerías y utilidades
│   ├── api.ts                # Cliente axios configu rado
│   └── hooks.ts              # Hooks de React Query
├── hooks/                    # Custom hooks
│   └── useAuth.ts            # Hook de autenticación
├── types/                    # Tipos TypeScript
│   └── index.ts
└── public/                   # Archivos estáticos
```

## Características

- ✅ Autenticación con JWT
- ✅ Gestión de categorías (CRUD)
- ✅ Gestión de productos (CRUD)
- ✅ Gestión de lotes/batches
- ✅ Visualización de movimientos
- ✅ Interfaz responsiva con Tailwind CSS
- ✅ Estado manejado con React Query
- ✅ TypeScript para mayor seguridad de tipos

## Flujo de Autenticación

1. Usuario se registra o inicia sesión
2. Se guarda el token JWT en localStorage
3. El token se envía automáticamente en los headers de cada petición
4. Si el token expira (401), se redirige a login

## API Endpoints Utilizados

### Autenticación
- `POST /auth/login/` - Iniciar sesión
- `POST /auth/register/` - Registrarse
- `POST /auth/token/refresh/` - Refrescar token
- `POST /auth/token/blacklist/` - Logout

### Categorías
- `GET /categories/` - Listar todas
- `GET /categories/<id>/` - Obtener una
- `POST /categories/` - Crear
- `PUT /categories/<id>/` - Actualizar
- `DELETE /categories/<id>/` - Eliminar

### Productos
- `GET /products/` - Listar todas
- `GET /products/<id>/` - Obtener uno
- `POST /products/` - Crear
- `PUT /products/<id>/` - Actualizar
- `DELETE /products/<id>/` - Eliminar

### Lotes/Batches
- `GET /batches/` - Listar todos
- `GET /batches/<id>/` - Obtener uno
- `POST /batches/` - Crear
- `PUT /batches/<id>/` - Actualizar
- `DELETE /batches/<id>/` - Eliminar

### Movimientos
- `GET /movements/` - Listar todos
- `GET /movements/<id>/` - Obtener uno
