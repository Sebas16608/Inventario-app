# ⚡ Guía Rápida: Setup Completo (Backend + Frontend)

**Tiempo estimado: 15 minutos**

## 📋 Pre-requisitos

- ✅ Node.js 18+ (`node --version`)
- ✅ Python 3.10+ (`python --version`)
- ✅ Git (`git --version`)

---

## 🔙 PASO 1: Backend Django

Already running? ✅ Skip to Step 2.

```bash
# 1. Entrar al directorio backend
cd backend

# 2. Crear entorno virtual (primera vez)
python -m venv ../.venv
source ../.venv/bin/activate  # Mac/Linux
# ..\.venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Migraciones
python manage.py migrate

# 5. Crear superuser (para admin)
python manage.py createsuperuser

# 6. Iniciar servidor
python manage.py runserver

# Verifica: http://localhost:8000/admin
```

Backend listo ✅ Abre otra terminal y continúa...

---

## 🎨 PASO 2: Frontend Next.js

```bash
# 1. Volver a la raíz del proyecto
cd ..

# 2. Ir al frontend
cd frontend

# 3. OPCIÓN A: Setup automático (recomendado)
./quickstart.sh

# OPCIÓN B: Manual
npm install
cp .env.example .env.local

# 4. Iniciar servidor
npm run dev

# Verifica: http://localhost:3000
```

Frontend listo ✅

---

## 🧪 PASO 3: Prueba la Aplicación

### Login/Registro
1. Abre http://localhost:3000
2. Haz clic en "Registrarse"
3. Llena el forma con:
   - Email: `test@example.com`
   - Username: `testuser`
   - Password: `Test123!`
   - Company: `Mi Empresa`

### Prueba Features
- **Categorías**: http://localhost:3000/categories
- **Productos**: http://localhost:3000/products
- **Movimientos**: http://localhost:3000/movements
- **Dashboard**: http://localhost:3000/dashboard

---

## 🚀 OPCIÓN: Correr Todo Junto

Desde la **raíz del proyecto**:

```bash
# Opción A: Script automático
./run-dev.sh

# Opción B: Manual (2 terminales)
# Terminal 1:
cd backend
source ../.venv/bin/activate
python manage.py runserver

# Terminal 2:
cd frontend
npm run dev
```

---

## 🐛 Troubleshooting

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError` | `pip install -r backend/requirements.txt` |
| `npm ERR!` | `rm -rf frontend/node_modules && npm install` |
| `Port 3000 already in use` | `lsof -i :3000` y mata el proceso |
| `Port 8000 already in use` | `lsof -i :8000` y mata el proceso |
| `Cannot GET /api/...` | Backend no está corriendo en :8000 |
| `JWT token invalid` | `localStorage.clear()` en DevTools |

---

## 📁 Estructura de Archivos Importantes

```
.
├── backend/
│   ├── manage.py          ← Django
│   ├── requirements.txt    ← Dependencias Python
│   ├── core/settings.py    ← Config base
│   └── .env               ← Variables de entorno
│
├── frontend/
│   ├── app/               ← Páginas
│   ├── package.json       ← Dependencias JS
│   ├── .env.local         ← Variables de entorno
│   └── quickstart.sh      ← Setup automático
│
└── .env                   ← Variables globales
```

---

## 📚 Documentación por Tema

| Necesitas | Archivo |
|----------|---------|
| Setup del Frontend | [FRONTEND_SETUP.md](FRONTEND_SETUP.md) |
| Lista de Features | [FRONTEND_SUMMARY.md](FRONTEND_SUMMARY.md) |
| Completar CRUD | [FRONTEND_CRUD_GUIDE.md](FRONTEND_CRUD_GUIDE.md) |
| Setup del Backend | [backend/README.md](backend/README.md) |
| Deploy a Producción | [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) |

---

## 🎯 Después del Setup

### Próximos pasos recomendados:
1. ✅ **Completar CRUD** de categorías/productos
2. ✅ **Agregar validaciones** con Zod
3. ✅ **Dashboard estadísticas**
4. ✅ **Gestión de lotes**
5. ✅ **Reportes y exportación**

Ver [FRONTEND_CRUD_GUIDE.md](FRONTEND_CRUD_GUIDE.md) para ejemplos de código.

---

## 💡 Tips Rápidos

### Ver logs del backend
```bash
cd backend
python manage.py runserver  # Sin "&" para ver logs
```

### Resetear base de datos
```bash
cd backend
python manage.py migrate zero  # Revert todas las migraciones
python manage.py migrate       # Aplicar de nuevo
```

### Limpiar localStorage en Frontend
```javascript
// En DevTools Console
localStorage.clear()
window.location.reload()
```

### Ver requests HTTP en DevTools
```
Network tab → Ver requests al backend
```

---

## ✅ Checklist Final

- [ ] Backend running en http://localhost:8000
- [ ] Frontend running en http://localhost:3000
- [ ] Puedo registrarme
- [ ] Puedo loguearme
- [ ] Veo categorías en `/categories`
- [ ] Veo productos en `/products`
- [ ] Veo movimientos en `/movements`

Si todos están ✅ **¡Éxito! Tu app está lista.** 🎉

---

**¿Problemas?** Revisa los archivos de documentación o pregunta en `backend/README.md` o `frontend/README.md`.
