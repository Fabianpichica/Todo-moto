from django.contrib import admin
from .models import Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('activa',)
    search_fields = ('nombre', 'descripcion')
    actions = None  # Desactiva acciones masivas como eliminar
    def has_delete_permission(self, request, obj=None):
        return False  # No permitir eliminar categorías
