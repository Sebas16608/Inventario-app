# Estilos y Buenas Prácticas

Guía de estilos, temas y mejores prácticas CSS/Tailwind para el frontend.

## 🎨 Sistema de Colores

### Esquema de Colores Principal

La aplicación utiliza un esquema de colores profesional basado en azul:

```
Primary (Azul)
├── 50:  #f0f9ff  (Fondo muy claro)
├── 100: #e0f2fe  (Fondo claro)
├── 200: #bae6fd  (Hover claro)
├── 300: #7dd3fc  (Acento suave)
├── 400: #38bdf8  (Acento)
├── 500: #0ea5e9  (Principal) ⭐
├── 600: #0284c7  (Hover principal)
├── 700: #0369a1  (Activo)
├── 800: #075985  (Oscuro)
└── 900: #082f49  (Muy oscuro)

Secondary (Gris)
├── 500: #6b7280
├── 600: #4b5563
├── 700: #374151
└── 800: #1f2937

Success (Verde)
├── 400: #4ade80
├── 500: #22c55e
├── 600: #16a34a
└── 700: #15803d

Warning (Amarillo)
├── 400: #facc15
├── 500: #eab308
├── 600: #ca8a04
└── 700: #a16207

Danger (Rojo)
├── 400: #f87171
├── 500: #ef4444
├── 600: #dc2626
└── 700: #b91c1c

Info (Azul Claro)
├── 400: #38bdf8
├── 500: #0ea5e9
├── 600: #0284c7
└── 700: #0369a1
```

### Uso de Colores

```tsx
// Fondo
<div className="bg-primary-50">       // Fondo muy claro
<div className="bg-white">             // Blanco

// Texto
<p className="text-gray-700">         // Texto principal
<p className="text-gray-500">         // Texto secundario
<p className="text-primary-600">      // Texto de acción

// Botones
<button className="bg-primary-500 hover:bg-primary-600">
<button className="bg-success-500 hover:bg-success-600">
<button className="bg-danger-500 hover:bg-danger-600">

// Estados
<div className="border-warning-300">  // Advertencia
<div className="border-danger-300">   // Error
<div className="border-success-300">  // Éxito
```

---

## 📏 Espaciado

### Sistema de Espaciado (Unidades de 4px)

```
0   → 0px
1   → 4px
2   → 8px
3   → 12px
4   → 16px   ← Espaciado estándar
5   → 20px
6   → 24px
8   → 32px
12  → 48px
16  → 64px
20  → 80px
```

### Convenciones de Espaciado

```tsx
// Contenedor principal
<div className="p-6">                 // Padding 24px (6 × 4)

// Elementos internos
<div className="space-y-4">           // Gap 16px vertical
<div className="space-x-3">           // Gap 12px horizontal

// Márgenes entre secciones
<section className="mb-8">            // Margin-bottom 32px

// Padding en inputs
<input className="px-4 py-2" />       // PadX 16px, PadY 8px

// Gap en grillas
<div className="gap-4">               // 16px gap entre items
```

---

## 🔤 Tipografía

### Escalas de Tamaño

```
text-xs    → 12px   (0.75rem)  - Pequeño
text-sm    → 14px   (0.875rem) - Pequeño
text-base  → 16px   (1rem)     - Normal ← Estándar
text-lg    → 18px   (1.125rem) - Grande
text-xl    → 20px   (1.25rem)  - Más grande
text-2xl   → 24px   (1.5rem)   - Título pequeño
text-3xl   → 30px   (1.875rem) - Título Segundo nivel
text-4xl   → 36px   (2.25rem)  - Título principal
```

### Pesos de Fuente

```
font-light    → 300  (Delgado)
font-normal   → 400  (Normal) ← Estándar
font-medium   → 500  (Semi-bold)
font-semibold → 600  (Bold)
font-bold     → 700  (Muy bold)
```

### Ejemplos de Tipografía

```tsx
// Títulos
<h1 className="text-4xl font-bold text-gray-900">Inventario</h1>
<h2 className="text-2xl font-semibold text-gray-800">Productos</h2>
<h3 className="text-lg font-semibold text-gray-700">Sección</h3>

// Textos principales
<p className="text-base text-gray-700">Contenido principal</p>

// Textos secundarios
<p className="text-sm text-gray-500">Información adicional</p>

// Etiquetas y labels
<label className="text-sm font-medium text-gray-700">Email</label>

// Links
<a href="#" className="text-primary-600 hover:text-primary-700 font-medium">
  Ver más
</a>
```

---

## 🎯 Componentes Consistentes

### Botones - Pattern

```tsx
// Primario (Acción principal)
<Button variant="primary">
  Guardar
</Button>
// Clases: bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-lg

// Secundario (Acción alternativa)
<Button variant="secondary">
  Cancelar
</Button>
// Clases: bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-lg

// Peligro (Acción destructiva)
<Button variant="danger">
  Eliminar
</Button>
// Clases: bg-danger-500 hover:bg-danger-600 text-white px-4 py-2 rounded-lg
```

### Cards - Pattern

```tsx
<Card>
  <div className="p-6 border-b border-gray-200">
    <h3 className="text-lg font-semibold text-gray-900">Título</h3>
  </div>
  
  <div className="p-6">
    <p className="text-gray-700">Contenido</p>
  </div>
  
  <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex gap-3">
    <Button>Acción</Button>
  </div>
</Card>
```

### Tablas - Pattern

```tsx
<table className="min-w-full divide-y divide-gray-200">
  <thead className="bg-gray-50">
    <tr>
      <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">
        Columna
      </th>
    </tr>
  </thead>
  
  <tbody className="divide-y divide-gray-200 bg-white">
    <tr className="hover:bg-gray-50">
      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
        Dato
      </td>
    </tr>
  </tbody>
</table>
```

### Formularios - Pattern

```tsx
<form className="space-y-6">
  <div>
    <label className="block text-sm font-medium text-gray-700 mb-2">
      Email
    </label>
    <Input
      type="email"
      placeholder="tu@email.com"
    />
  </div>

  <div>
    <label className="block text-sm font-medium text-gray-700 mb-2">
      Categoría
    </label>
    <Select options={categories} />
  </div>

  <div className="flex gap-3 pt-4">
    <Button variant="primary">Guardar</Button>
    <Button variant="secondary">Cancelar</Button>
  </div>
</form>
```

---

## 📋 Estilos por Sección

### Navbar

```tsx
<nav className="bg-white border-b border-gray-200 sticky top-0 z-40">
  <div className="px-6 py-4 flex items-center justify-between">
    <div className="text-2xl font-bold text-primary-600">Inventario</div>
    
    <ul className="flex gap-6">
      <li>
        <a href="#" className="text-gray-700 hover:text-primary-600 font-medium">
          Dashboard
        </a>
      </li>
    </ul>
    
    <div className="flex items-center gap-4">
      {/* User menu */}
    </div>
  </div>
</nav>
```

### Sidebar (si aplica)

```tsx
<aside className="w-64 bg-gray-50 border-r border-gray-200 min-h-screen">
  <div className="p-6">
    <h1 className="text-2xl font-bold text-primary-600">Inventario</h1>
  </div>
  
  <nav className="mt-6 space-y-2 px-4">
    <a href="#" className="block px-4 py-2 rounded-lg bg-primary-50 text-primary-600 font-medium">
      Dashboard
    </a>
  </nav>
</aside>
```

### Main Content Area

```tsx
<main className="flex-1 bg-gray-50 p-6">
  <div className="max-w-7xl mx-auto">
    <header className="mb-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">Productos</h1>
      <p className="text-gray-600">Gestiona tu inventario de productos</p>
    </header>

    <div className="bg-white rounded-lg shadow-sm p-6">
      {/* Contenido */}
    </div>
  </div>
</main>
```

---

## 🔷 Sombras y Bordes

### Sombras

```
shadow-none  → sin sombra
shadow-sm    → sombra muy pequeña (cards)
shadow       → sombra estándar
shadow-md    → sombra media
shadow-lg    → sombra grande (modales)
shadow-xl    → sombra muy grande
```

### Uso de Sombras

```tsx
// Cards
<div className="bg-white rounded-lg shadow-sm p-6">

// Elementos flotantes
<div className="fixed bg-white shadow-lg rounded-lg">

// Sin sombra (flat design)
<div className="bg-white border border-gray-200 p-6">
```

### Bordes

```
border       → 1px border
border-2     → 2px border

border-gray-200  → Bordes sutiles (divisiones)
border-gray-300  → Bordes estándar (inputs)
border-primary-300  → Bordes de acción

rounded      → 4px radio
rounded-lg   → 8px radio (estándar)
rounded-xl   → 12px radio
```

---

## 🎬 Animaciones y Transiciones

### Transiciones Estándar

```tsx
// Hover suave
<button className="transition duration-200 hover:bg-primary-600">
  Botón
</button>

// Fade in
<div className="transition duration-500 opacity-0 data-[enter]:opacity-100">
  Contenido
</div>

// Escala
<div className="transform transition hover:scale-105">
  Logo
</div>
```

### Efectos

```tsx
// Hover de texto
<a className="text-primary-600 hover:text-primary-700 transition">Link</a>

// Hover de fondo
<div className="bg-gray-50 hover:bg-gray-100 transition">Item</div>

// Clic activo
<button className="active:scale-95 transition">Presionar</button>

// Carga
<div className="animate-spin">⏳</div>
<div className="animate-pulse">Parpadeando</div>
```

---

## 📱 Responsividad

### Breakpoints

```
mobile   → 0px - 640px   (sm)
tablet   → 640px - 1024px (md)
desktop  → 1024px+       (lg)
wide     → 1280px+       (xl)
```

### Patrones Responsive

```tsx
// Grid responsivo
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* Items */}
</div>

// Texto responsivo
<h1 className="text-2xl md:text-3xl lg:text-4xl">Título</h1>

// Padding responsivo
<div className="p-4 md:p-6 lg:p-8">Contenido</div>

// Display responsivo
<button className="md:hidden">Menú móvil</button>
<nav className="hidden md:flex">Menú desktop</nav>
```

---

## 🌙 Modo Oscuro (Futuro)

Si se implementa modo oscuro, usar clases como:

```tsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  Contenido
</div>
```

---

## ⚠️ Estados Visuales

### Estados Comunes

```tsx
// Deshabilitado
<button disabled className="opacity-50 cursor-not-allowed">
  Inactivo
</button>

// Cargando
<button className="opacity-75 pointer-events-none">
  <span className="inline-block animate-spin mr-2">⏳</span>
  Cargando...
</button>

// Éxito
<div className="bg-success-50 border border-success-200 text-success-800 p-4 rounded-lg">
  ✅ Guardado exitosamente
</div>

// Error
<div className="bg-danger-50 border border-danger-200 text-danger-800 p-4 rounded-lg">
  ❌ Error: Campo requerido
</div>

// Advertencia
<div className="bg-warning-50 border border-warning-200 text-warning-800 p-4 rounded-lg">
  ⚠️ Advertencia: cambios sin guardar
</div>

// Información
<div className="bg-info-50 border border-info-200 text-info-800 p-4 rounded-lg">
  ℹ️ Información: se mostrará a todos
</div>
```

---

## 🎯 Layout Patterns

### Container

```tsx
<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  {/* Contenido con máximo ancho y centrado */}
</div>
```

### Two Column

```tsx
<div className="grid grid-cols-1 md:grid-cols-3 gap-6">
  <aside className="md:col-span-1">
    {/* Sidebar */}
  </aside>
  <main className="md:col-span-2">
    {/* Contenido principal */}
  </main>
</div>
```

### Three Column

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* Items */}
</div>
```

### Flexbox

```tsx
// Items horizontales
<div className="flex gap-4">
  {/* Items */}
</div>

// Items con wrap
<div className="flex flex-wrap gap-4">
  {/* Tags/pills */}
</div>

// Centrado completo
<div className="flex items-center justify-center h-screen">
  {/* Contenido centrado */}
</div>
```

---

## 💡 Buenas Prácticas

### ✅ DO

```tsx
// 1. Usar clases de utility
<div className="p-4 bg-white rounded-lg shadow-sm">

// 2. Agrupar por tipo
<div className="flex gap-4 items-center">

// 3. Usar componentes para patrones repetidos
<Button variant="primary">Acción</Button>

// 4. Responsive mobile-first
<div className="w-full md:w-1/2 lg:w-1/3">
```

### ❌ DON'T

```tsx
// 1. Estilos inline
<div style={{ padding: '16px', backgroundColor: 'white' }}>

// 2. CSS personalizado cuando hay utility
<style>{`.my-btn { @apply px-4 py-2 bg-blue-500; }`}</style>

// 3. Clases sin contexto
<div className="text-blue-500 hover:text-blue-600 bg-gray-100 p-4">

// 4. Desktop-first en responsive
<div className={isMobile ? 'w-full' : 'w-1/3'}>
```

---

## 🔄 Consistencia de Espaciado

### Márgenes Externas
- Entre secciones: `mb-8` (32px)
- Entre componentes: `mb-6` (24px)
- Entre elementos: `mb-4` (16px)
- Entre items pequeños: `mb-2` (8px)

### Padding Interno
- Contenedor principal: `p-6` (24px)
- Componente: `p-4` (16px)
- Elemento pequeño: `p-2` (8px)

### Gaps en Flexbox/Grid
- Entre elementos principales: `gap-6` (24px)
- Entre elementos secundarios: `gap-4` (16px)
- Entre items pequeños: `gap-2` (8px)

---

## 📊 Ejemplo de Página Completa

```tsx
export default function ProductsPage() {
  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-900">Productos</h1>
          <Button>Nuevo Producto</Button>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Input placeholder="Buscar..." />
            <Select options={categories} />
            <Button>Filtrar</Button>
          </div>
        </div>

        {/* Results */}
        <div className="rounded-lg shadow-sm overflow-hidden bg-white">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">
                  Producto
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">
                  Categoría
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">
                  Precio
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {/* Rows */}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  )
}
```

---

## 🎨 Paleta de Colores Rápida

Para copiar y pegar en componentes:

```tsx
// Fondos
bg-white              // Blanco
bg-gray-50            // Gris muy claro
bg-gray-100           // Gris claro
bg-primary-50         // Blue muy claro
bg-primary-500        // Blue principal

// Textos
text-white            // Blanco
text-gray-900         // Negro/Oscuro
text-gray-700         // Gris oscuro
text-gray-500         // Gris medio
text-primary-600      // Blue

// Bordes
border-gray-200       // Gris claro
border-gray-300       // Gris medio
border-primary-300    // Blue claro
border-danger-300     // Rojo claro

// Hover
hover:bg-gray-50      // Fondo hover gris
hover:bg-primary-600  // Botón hover
hover:text-primary-600  // Link hover
```

---

## 🚀 Optimizaciones

1. **Evitar overflow de clases** - Usar @apply en Tailwind si hay 10+ clases
2. **Purgar CSS no usado** - Tailwind elimina clases que no se usan
3. **Lazy load imágenes** - `loading="lazy"` en <img>
4. **Minimizar repaint** - `transform` y `opacity` en lugar de cambiar dimensiones
5. **Z-index consistente** - Navnar: 40, Modal: 50, Tooltip: 60
