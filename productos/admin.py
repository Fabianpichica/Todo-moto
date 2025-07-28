# productos/admin.py
from django.contrib import admin
from .models import Producto, CarritoItem   

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'disponible', 'fecha_creacion')
    list_filter = ('disponible', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'stock', 'disponible')

@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'producto', 'cantidad', 'fecha_agregado', 'get_total_item_price')
    list_filter = ('usuario', 'fecha_agregado')
    search_fields = ('usuario__username', 'producto__nombre')
    readonly_fields = ('fecha_agregado',)
