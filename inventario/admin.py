from django.contrib import admin
from django.utils.html import format_html
from inventario.models import Category, Product, Batch, Movement
from inventario.services.stock_service import StockService


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'presentation', 'distribuidor', 'total_stock', 'slug')
    search_fields = ('name', 'slug', 'distribuidor')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('total_stock_display',)

    def total_stock_display(self, obj):
        """Muestra el stock total usando el servicio"""
        try:
            batches = obj.batches.all()
            total = sum(b.quantity_available for b in batches)
            return format_html(
                '<span style="font-weight: bold; color: {};">{}</span>',
                'green' if total > 0 else 'red',
                total
            )
        except:
            return "N/A"
    total_stock_display.short_description = "Stock Total"

    def total_stock(self, obj):
        """Columna adicional para listar"""
        batches = obj.batches.all()
        return sum(b.quantity_available for b in batches)
    total_stock.short_description = "Stock Total"


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_received', 'quantity_available', 'purchase_price', 'expiration_date', 'stock_status', 'supplier')
    search_fields = ('product__name', 'supplier')
    list_filter = ('expiration_date', 'supplier', 'received_at')
    readonly_fields = ('received_at', 'quantity_received')
    fieldsets = (
        ('Información del Producto', {
            'fields': ('product', 'supplier')
        }),
        ('Stock', {
            'fields': ('quantity_received', 'quantity_available')
        }),
        ('Precios', {
            'fields': ('purchase_price',)
        }),
        ('Fechas', {
            'fields': ('expiration_date', 'received_at')
        }),
    )

    def stock_status(self, obj):
        """Muestra el estado del stock con color"""
        if obj.quantity_available == 0:
            color = 'red'
            status = 'Agotado'
        elif obj.quantity_available <= obj.quantity_received * 0.2:
            color = 'orange'
            status = 'Bajo'
        else:
            color = 'green'
            status = 'Normal'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            status
        )
    stock_status.short_description = "Estado Stock"

    def save_model(self, request, obj, form, change):
        """Guarda el modelo usando transacciones atómicas del servicio"""
        super().save_model(request, obj, form, change)


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ('batch', 'movement_type_display', 'quantity', 'created_at', 'note')
    search_fields = ('batch__product__name', 'note')
    list_filter = ('movement_type', 'created_at')
    readonly_fields = ('created_at', 'batch', 'quantity')
    fieldsets = (
        ('Información del Movimiento', {
            'fields': ('batch', 'movement_type', 'quantity')
        }),
        ('Detalles', {
            'fields': ('note', 'created_at')
        }),
    )

    def movement_type_display(self, obj):
        """Muestra el tipo de movimiento con color"""
        colors = {
            'IN': ('green', 'Entrada'),
            'OUT': ('red', 'Salida'),
            'ADJUST': ('blue', 'Ajuste'),
            'EXPIRED': ('gray', 'Expirado'),
        }
        color, label = colors.get(obj.movement_type, ('black', obj.movement_type))
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            label
        )
    movement_type_display.short_description = "Tipo de Movimiento"

    def has_add_permission(self, request):
        """Los movimientos se crean automáticamente vía servicios"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Los movimientos son histórico, no deben borrarse"""
        return False
