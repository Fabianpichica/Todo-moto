# productos/admin.py
from django.contrib import admin
from .models import Producto, CarritoItem, Pedido
from .forms import ProductoAdminForm

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    form = ProductoAdminForm
    list_display = ('nombre', 'precio', 'stock', 'disponible', 'fecha_creacion')
    list_filter = ('disponible', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'disponible')
    readonly_fields = ('stock',)

@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'producto', 'cantidad', 'fecha_agregado', 'get_total_item_price')
    list_filter = ('usuario', 'fecha_agregado')
    search_fields = ('usuario__username', 'producto__nombre')
    readonly_fields = ('fecha_agregado',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'usuario', 'estado', 'total_pedido', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion', 'ciudad')
    search_fields = ('nombre', 'usuario__username', 'direccion', 'ciudad')
    list_editable = ('estado',)
    readonly_fields = ('fecha_creacion',)
