from django.urls import path
from inventario.views.category_view import CategoryAPIView
from inventario.views.product_view import ProductAPIView
from inventario.views.stock_view import StockInView, StockOutView

urlpatterns = [
    # Categories
    path("categories/", CategoryAPIView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryAPIView.as_view(), name="category-detail"),

    # Products
    path("products/", ProductAPIView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductAPIView.as_view(), name="product-detail"),

    # Stock
    path(
        "products/<int:product_id>/stock/in/",
        StockInView.as_view(),
        name="stock-in",
    ),
    path(
        "products/<int:product_id>/stock/out/",
        StockOutView.as_view(),
        name="stock-out",
    ),
]
