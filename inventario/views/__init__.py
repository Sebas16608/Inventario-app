"""
Inventario app views.

Secure multi-tenant API views with company isolation.
"""

from inventario.views.base_views import BaseCompanyAPIView
from inventario.views.category_view import CategoryAPIView
from inventario.views.product_view import ProductAPIView
from inventario.views.batch_view import BatchAPIView
from inventario.views.movement_view import MovementAPIView
from inventario.views.stock_view import StockInView, StockOutView

__all__ = [
    'BaseCompanyAPIView',
    'CategoryAPIView',
    'ProductAPIView',
    'BatchAPIView',
    'MovementAPIView',
    'StockInView',
    'StockOutView',
]
