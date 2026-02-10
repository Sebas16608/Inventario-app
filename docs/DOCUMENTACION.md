# 📚 Índice de Documentación - Inventario App

Bienvenido a Inventario App. Esta es tu guía para navegar toda la documentación del proyecto.

---

## 🚀 Comenzar Rápido

1. **Primeros Pasos**: [README.md](README.md)
2. **Instalación Detallada**: [INSTALACION.md](INSTALACION.md)
3. **Primeros Requests a API**: [API.md](API.md#-casos-de-uso-comunes)

---

## 📖 Documentación Completa

### Para Entender el Proyecto

| Documento | Propósito | Audiencia |
|-----------|-----------|-----------|
| [README.md](README.md) | Introducción y features principales | Todos |
| [ARQUITECTURA.md](ARQUITECTURA.md) | Estructura técnica y diseño | Desarrolladores |
| [MODELOS.md](MODELOS.md) | Modelos de datos y relaciones | Desarrolladores/DBA |
| [ROADMAP.md](ROADMAP.md) | Plan de desarrollo futuro | Product/Gerentes |

### Para Usar la Aplicación

| Documento | Propósito | Audiencia |
|-----------|-----------|-----------|
| [API.md](API.md) | Todos los endpoints disponibles | Desarrolladores frontend/integradores |
| [INSTALACION.md](INSTALACION.md) | Setup y deployment | DevOps/System Admin |
| [PREGUNTAS_FRECUENTES.md](PREGUNTAS_FRECUENTES.md) | Troubleshooting común | Todos |

### Para Contribuir

| Documento | Propósito | Audiencia |
|-----------|-----------|-----------|
| [DESARROLLO.md](DESARROLLO.md) | Guía de desarrollo local | Desarrolladores |
| [CONTRIBUCIONES.md](CONTRIBUCIONES.md) | Proceso de contribución | Contributors |

---

## 🗂️ Flujo por Rol

### 👨‍💼 Product Manager / Gerente

1. [README.md](README.md) - Features y visión
2. [ROADMAP.md](ROADMAP.md) - Plan de desarrollo
3. [PREGUNTAS_FRECUENTES.md](PREGUNTAS_FRECUENTES.md) - Casos comunes

### 💻 Desarrollador Backend

1. [README.md](README.md) - Overview
2. [INSTALACION.md](INSTALACION.md) - Setup local
3. [ARQUITECTURA.md](ARQUITECTURA.md) - Estructura
4. [MODELOS.md](MODELOS.md) - Modelos de datos
5. [DESARROLLO.md](DESARROLLO.md) - Guía de desarrollo
6. [CONTRIBUCIONES.md](CONTRIBUCIONES.md) - Estándares

### 🎨 Desarrollador Frontend

1. [README.md](README.md) - Overview
2. [API.md](API.md) - Especificación de endpoints
3. [MODELOS.md](MODELOS.md) - Estructura de datos
4. [PREGUNTAS_FRECUENTES.md](PREGUNTAS_FRECUENTES.md) - Troubleshooting

### 🔧 DevOps / System Admin

1. [INSTALACION.md](INSTALACION.md) - Setup completo
2. [ARQUITECTURA.md](ARQUITECTURA.md) - Decisiones técnicas
3. [DESARROLLO.md](DESARROLLO.md) - Comandos útiles

### 🐛 QA / Tester

1. [README.md](README.md) - Features a testear
2. [API.md](API.md) - Endpoints y casos de uso
3. [PREGUNTAS_FRECUENTES.md](PREGUNTAS_FRECUENTES.md) - Problemas comunes

---

## 📋 Checklist por Tarea

### ✅ Instalar en Desarrollo
- [ ] Leer [README.md](README.md) - Quick Start
- [ ] Seguir [INSTALACION.md](INSTALACION.md)
- [ ] Crear `.env` basado en `.env.example`
- [ ] Ejecutar migraciones
- [ ] Verificar servidor corre en localhost:8000

### ✅ Hacer un Request a la API
- [ ] Obtener token JWT ([API.md - Autenticación](API.md#-autenticación))
- [ ] Crear categoría y producto ([API.md - Casos de Uso](API.md#-casos-de-uso-comunes))
- [ ] Verificar respuesta 201 Created

### ✅ Crear Nueva Feature
- [ ] Leer [DESARROLLO.md - Crear Nuevo Modelo](DESARROLLO.md#-crear-un-nuevo-modelo)
- [ ] Implementar modelo, serializer, vista
- [ ] Escribir tests
- [ ] Hacer PR siguiendo [CONTRIBUCIONES.md](CONTRIBUCIONES.md)

### ✅ Resolver un Bug
- [ ] Reproducir bug según pasos
- [ ] Encontrar código afectado
- [ ] Escribir test que falla
- [ ] Arreglar código
- [ ] Verificar test pasa
- [ ] Hacer PR con descripción clara

### ✅ Deployar a Producción
- [ ] Seguir [INSTALACION.md - Deployment](INSTALACION.md#-instalación-en-servidor-producción)
- [ ] Configurar Gunicorn
- [ ] Configurar Nginx
- [ ] Configurar Systemd
- [ ] Verificar SSL/HTTPS
- [ ] Configurar backups

### ✅ Reportar un Problema
- [ ] Verificar en [PREGUNTAS_FRECUENTES.md](PREGUNTAS_FRECUENTES.md)
- [ ] Si no está, crear Issue en GitHub
- [ ] Incluir pasos para reproducir
- [ ] Agregar logs/mensajes de error
- [ ] Mencionar versiones (Python, Django, OS)

---

## 🔍 Buscar Información

### Por Tema

**Modelos de Datos**
→ [MODELOS.md](MODELOS.md)

**Endpoints API**
→ [API.md](API.md)

**Arquitectura Sistema**
→ [ARQUITECTURA.md](ARQUITECTURA.md)

**Como Desarrollar**
→ [DESARROLLO.md](DESARROLLO.md)

**Como Instalar/Deployar**
→ [INSTALACION.md](INSTALACION.md)

**Problemas Comunes**
→ [PREGUNTAS_FRECUENTES.md](PREGUNTAS_FRECUENTES.md)

**Proceso de Contribución**
→ [CONTRIBUCIONES.md](CONTRIBUCIONES.md)

**Plan Futuro**
→ [ROADMAP.md](ROADMAP.md)

### Por Palabra Clave

| Palabra Clave | Documento |
|---------------|-----------|
| JWT, Token, Autenticación | [API.md](API.md) |
| Product, Category, Batch, Movement | [MODELOS.md](MODELOS.md) |
| Migración, Test, Models | [DESARROLLO.md](DESARROLLO.md) |
| PostgreSQL, Gunicorn, Nginx | [INSTALACION.md](INSTALACION.md) |
| Relaciones, Multi-tenancy | [ARQUITECTURA.md](ARQUITECTURA.md) |
| Error, Bug, No funciona | [PREGUNTAS_FRECUENTES.md](PREGUNTAS_FRECUENTES.md) |

---

## 📞 Links Rápidos

### Importante
- **GitHub Repo**: https://github.com/Sebas16608/Inventario-app
- **Issues**: https://github.com/Sebas16608/Inventario-app/issues
- **Discussions**: https://github.com/Sebas16608/Inventario-app/discussions

### Documentación Externa
- **Django Docs**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **JWT**: https://jwt.io/

### Herramientas Útiles
- **Postman**: https://www.postman.com/ (Testing API)
- **DBeaver**: https://dbeaver.io/ (DB Management)
- **VS Code**: https://code.visualstudio.com/ (Editor)

---

## 🎯 Matriz de Decisión

¿No sabes por dónde empezar? Usa esta matriz:

```
¿Eres nuevo en el proyecto?
├─ Sí
│  └─ Leer README.md → INSTALACION.md
│
¿Necesitas instalar?
├─ Sí → INSTALACION.md
│
¿Vas a desarrollar?
├─ Sí → DESARROLLO.md
│
¿Necesitas llamar API?
├─ Sí → API.md
│
¿Necesitas entender estructura?
├─ Sí → ARQUITECTURA.md + MODELOS.md
│
¿Tienes un problema?
├─ Sí → PREGUNTAS_FRECUENTES.md
│
¿Vas a contribuir?
├─ Sí → CONTRIBUCIONES.md
│
¿Quieres saber el plan?
└─ Sí → ROADMAP.md
```

---

## 📈 Progresión de Aprendizaje

### Nivel 1: Principiante
```
README.md
    ↓
INSTALACION.md (setup local)
    ↓
API.md (hacer requests)
    ↓
PREGUNTAS_FRECUENTES.md (resolver problemas)
```

### Nivel 2: Intermedio
```
ARQUITECTURA.md (entender diseño)
    ↓
MODELOS.md (entender datos)
    ↓
DESARROLLO.md (crear features)
    ↓
Tests unitarios
```

### Nivel 3: Avanzado
```
CONTRIBUCIONES.md (estándares código)
    ↓
Optimización performance
    ↓
Deployment en producción
    ↓
ROADMAP.md (visión futura)
```

---

## 🚀 Video Tutoriales (Próximamente)

- [ ] Setup inicial en 5 minutos
- [ ] Primer request a API
- [ ] Crear producto/venta
- [ ] Reportes de inventario
- [ ] Deploy en servidor

---

## 📊 Estadísticas de Documentación

| Métrica | Valor |
|---------|-------|
| **Documentos** | 9 archivos .md |
| **Páginas** | ~50 páginas equivalentes |
| **Ejemplos de Código** | 100+ |
| **Endpoints Documentados** | 30+ |
| **Casos de Uso** | 15+ |
| **FAQ** | 60+ preguntas |

---

## 🔄 Mantenimiento de Documentación

### Actualización Regular
- Cada release → Actualizar ROADMAP.md
- Cambios en API → Actualizar API.md
- Nuevo modelo → Actualizar MODELOS.md
- Cambio en setup → Actualizar INSTALACION.md

### Reporte de Errores en Docs
Si encuentras errores o incompletudes:
1. Crear issue con tag `documentation`
2. Describir el problema
3. Sugerir corrección

---

## 💡 Tips de Uso

### En VS Code
```bash
# Instalar extensión Markdown Preview
# Ctrl/Cmd + Shift + V para preview
# Ctrl/Cmd + Click en links para navegar
```

### Búsqueda Rápida
```bash
# En terminal, buscar en documentación
grep -r "palabra" *.md

# Ejemplos:
grep -r "PostgreSQL" *.md
grep -r "Token JWT" *.md
```

### Generar PDF
```bash
# Con pandoc
pandoc *.md -o Documentacion_Completa.pdf

# En VS Code con extensión "Markdown PDF"
```

---

## ✅ Checklist de Onboarding

- [ ] Leí README.md
- [ ] Instalé el proyecto localmente
- [ ] Entiendo la arquitectura (ARQUITECTURA.md)
- [ ] Conozco los modelos (MODELOS.md)
- [ ] Puedo hacer requests a API (API.md)
- [ ] Sé cómo desarrollar nuevas features (DESARROLLO.md)
- [ ] Entiendo el proceso de contribución (CONTRIBUCIONES.md)
- [ ] He revisado roadmap (ROADMAP.md)

---

## 🎓 Recursos de Aprendizaje

### Django
- [Official Django Tutorial](https://docs.djangoproject.com/en/6.0/intro/tutorial01/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)

### Django REST Framework
- [DRF Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/)
- [DRF Best Practices](https://www.django-rest-framework.org/topics/documentation/)

### PostgreSQL
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- [SQL Basics](https://www.w3schools.com/sql/)

---

**Última actualización**: 10 de febrero de 2026

*¿Necesitas ayuda? Abre un issue o crea una discussion en GitHub.*
