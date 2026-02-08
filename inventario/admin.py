from django.contrib import admin
from inventario.models import Category, Product, Batch, Movement


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'presentation', 'distribuidor', 'slug')
    search_fields = ('name', 'slug', 'distribuidor')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_received', 'quantity_available', 'purchase_price', 'expiration_date', 'supplier')
    search_fields = ('product__name', 'supplier')
    list_filter = ('expiration_date', 'supplier', 'received_at')
    readonly_fields = ('received_at',)


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ('batch', 'movement_type', 'quantity', 'created_at')
    search_fields = ('batch__product__name',)
    list_filter = ('movement_type', 'created_at')
    readonly_fields = ('created_at',)
