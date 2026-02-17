# Guía de Contribuciones - Inventario App

## 🤝 ¿Cómo Contribuir?

¡Gracias por tu interés en contribuir a Inventario App! Aquí encontrarás las pautas para hacerlo.

---

## 📋 Proceso de Contribución

### 1. Fork del Repositorio

```bash
# Ir a GitHub y hacer fork del repositorio
# Luego clonar tu fork localmente
git clone https://github.com/TU_USUARIO/Inventario-app.git
cd Inventario-app
```

### 2. Crear una Rama Feature

```bash
# Crear rama desde main
git checkout -b feature/descripcion-corta

# Ejemplos de nombres buenos:
# - feature/agregar-autenticacion
# - fix/corregir-calculo-stock
# - docs/actualizar-readme
# - refactor/mejorar-services
```

### 3. Hacer Cambios

- Seguir [Estándares de Código](#estándares-de-código)
- Escribir tests para nuevas funcionalidades
- Actualizar documentación
- Hacer commits con mensajes descriptivos

```bash
git add archivo_modificado.py
git commit -m "feat: agregar validación de stock

- Validar cantidad disponible antes de venta
- Retornar error 400 si no hay stock
- Agregar tests unitarios"
```

### 4. Push a tu Fork

```bash
git push origin feature/descripcion-corta
```

### 5. Crear Pull Request

- Ir a GitHub
- Click en "New Pull Request"
- Llenar descripción clara
- Esperar revisión

---

## 📝 Estándares de Código

### Nombrado de Variables y Funciones

```python
# ✅ BIEN
def calcular_stock_disponible(producto_id):
    cantidad_total = 0
    for lote in Batch.objects.filter(product_id=producto_id):
        cantidad_total += lote.quantity_available
    return cantidad_total

# ❌ MAL
def calc_stock(pId):
    qt = 0
    for b in Batch.objects.filter(product_id=pId):
        qt += b.qty_avl
    return qt
```

### Importaciones

```python
# Orden correcto:
# 1. Librerías estándar
import os
import sys
from typing import Optional

# 2. Dependencias externas
from django.db import models
from rest_framework import serializers

# 3. Apps locales
from inventario.models import Product
from accounts.models import Company
```

### Formato de Código

Se recomienda usar **Black** for code formatting:

```bash
pip install black
black inventario/
```

### Type Hints

```python
# ✅ CON TYPE HINTS
def crear_movimiento(batch_id: int, cantidad: int, tipo: str) -> Movement:
    batch = Batch.objects.get(id=batch_id)
    movement = Movement.objects.create(
        batch=batch,
        quantity=cantidad,
        movement_type=tipo
    )
    return movement

# ❌ SIN TYPE HINTS
def crear_movimiento(batch_id, cantidad, tipo):
    batch = Batch.objects.get(id=batch_id)
    return Movement.objects.create(batch=batch, quantity=cantidad, movement_type=tipo)
```

### Docstrings

```python
def procesar_venta(producto_id: int, cantidad: int, cliente_id: int) -> dict:
    """
    Procesa una venta de producto.
    
    Valida disponibilidad de stock, registra el movimiento y retorna
    información de la transacción.
    
    Args:
        producto_id (int): ID del producto a vender
        cantidad (int): Cantidad a vender (debe ser > 0)
        cliente_id (int): ID del cliente comprador
    
    Returns:
        dict: {
            'success': bool,
            'movement_id': int o None,
            'message': str,
            'available_stock': int
        }
    
    Raises:
        Product.DoesNotExist: Si producto no existe
        ValueError: Si cantidad <= 0
        InsufficientStockError: Si no hay stock disponible
    
    Examples:
        >>> resultado = procesar_venta(1, 5, 10)
        >>> if resultado['success']:
        ...     print(f"Venta registrada: {resultado['movement_id']}")
    """
    pass
```

---

## ✅ Tests

### Escribir Tests Unitarios

```python
# En inventario/tests.py o tests/test_movements.py

from django.test import TestCase
from inventario.models import Product, Batch, Movement
from accounts.models import Company

class MovementTestCase(TestCase):
    def setUp(self):
        """Configurar datos de prueba"""
        self.company = Company.objects.create(name="Test Co")
        # ... más setup
    
    def test_crear_movimiento_salida(self):
        """Probar creación de movimiento OUT"""
        batch = Batch.objects.create(
            product_id=1,
            quantity_received=100,
            quantity_available=100,
            purchase_price=10.0,
            expiration_date="2025-12-31"
        )
        
        movement = Movement.objects.create(
            batch=batch,
            movement_type="OUT",
            quantity=10
        )
        
        self.assertEqual(movement.movement_type, "OUT")
        self.assertEqual(movement.quantity, 10)
    
    def test_no_permitir_cantidad_negativa(self):
        """Probar que no se permita cantidad negativa"""
        batch = Batch.objects.create(...)
        
        with self.assertRaises(ValueError):
            Movement.objects.create(
                batch=batch,
                movement_type="OUT",
                quantity=-5  # ❌ Inválido
            )
```

### Ejecutar Tests

```bash
# Todos los tests
python manage.py test

# Tests específicos
python manage.py test inventario.tests.MovementTestCase

# Con coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 📚 Documentación

### Actualizar Documentación

Si agregues una característica nueva, actualiza:

1. **README.md** - Si es un cambio mayor
2. **API.md** - Si agrega/modifica endpoints
3. **MODELOS.md** - Si modifica modelos
4. **DESARROLLO.md** - Si afecta el flujo de desarrollo

### Formato de Documentación

```markdown
## Título de Sección

Descripción clara y concisa.

### Subsección

Más detalles.

**Ejemplo:**
```python
# Código de ejemplo
```

**Respuesta esperada:**
```json
{"resultado": "ejemplo"}
```
```

---

## 🔍 Checklist Pre-Commit

Antes de hacer push, verifica:

- [ ] Tests pasan: `python manage.py test`
- [ ] Sin errores de linting: `pylint inventario/`
- [ ] Código formateado: `black inventario/`
- [ ] Docstrings presentes en funciones
- [ ] README/docs actualizados si es necesario
- [ ] Commits con mensajes descriptivos
- [ ] Sin credenciales o secretos en el código
- [ ] Migraciones creadas si se modifican modelos: `makemigrations`

---

## 🐛 Reportar Bugs

### Crear Issue

1. Ir a GitHub → Issues → New Issue
2. Usar título descriptivo
3. Proporcionar pasos para reproducir
4. Incluir versión Python, Django, OS
5. Agregar screenshots/logs si es relevante

### Plantilla de Bug Report

```markdown
## Descripción del Bug

Breve descripción del problema.

## Pasos para Reproducir

1. Hacer esto
2. Luego esto
3. Entonces pasa esto

## Comportamiento Esperado

Qué debería pasar.

## Comportamiento Actual

Qué pasa realmente.

## Información del Sistema

- Python: 3.10
- Django: 5.1.5
- Sistema Operativo: Ubuntu 22.04

## Logs/Error Messages

```
Tu error aquí
```
```

---

## 🎯 Sugerencias de Características

### Feature Requests

Crear issue con: 
- Descripción clara de la característica
- Caso de uso/beneficio
- Posible implementación (opcional)

---

## 📦 Versionado

Follows Semantic Versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Cambios incompatibles (breaking changes)
- **MINOR**: Nuevas características compatibles
- **PATCH**: Bug fixes

---

## 🚀 Proceso de Release

Solo para mantenedores:

```bash
# 1. Actualizar versión en __init__.py
# 2. Crear release branch
git checkout -b release/v1.0.0

# 3. Hacer cambios finales
# 4. Crear tag
git tag -a v1.0.0 -m "Versión 1.0.0"

# 5. Push
git push origin release/v1.0.0 --tags
```

---

## 🎓 Recursos Útiles

- [Django Docs](https://docs.djangoproject.com/)
- [DRF Docs](https://www.django-rest-framework.org/)
- [Git Guidelines](https://git-scm.com/book/en/v2)
- [Python PEP 8](https://pep8.org/)

---

## ❓ Preguntas?

Abre una Discussion en GitHub o contacta al mantenedor.

---

**¡Gracias por contribuir a Inventario App!** 🙌

**Última actualización**: 10 de febrero de 2026
