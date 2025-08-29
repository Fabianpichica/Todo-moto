# dashboard_admin/models.py
from django.db import models

# Si ya tienes un modelo Producto en la app 'productos',
# no necesitas definirlo aquí de nuevo.
# Asegúrate de que tu modelo Producto tenga un ForeignKey a Categoria si lo deseas.

class Categoria(models.Model):
    """
    Modelo para representar una categoría de productos.
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Última Actualización")
    activa = models.BooleanField(default=True, verbose_name="¿Activa?")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre'] # Ordenar categorías por nombre por defecto

    def __str__(self):
        """
        Representación en cadena del objeto Categoría.
        """
        return self.nombre