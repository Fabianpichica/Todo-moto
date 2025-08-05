
from django.db import models
from django.conf import settings
from productos.models import Producto

class MovimientoInventario(models.Model):
    # Tipos de movimiento: Entrada para agregar stock, Salida para quitarlo.
    TIPO_MOVIMIENTO_CHOICES = [
        ('Entrada', 'Entrada'),
        ('Salida', 'Salida'),
    ]

    # Motivos específicos para los movimientos
    MOTIVO_CHOICES = [
        ('Compra a proveedor', 'Compra a proveedor'),
        ('Novedad (daño, pérdida)', 'Novedad (daño, pérdida)'),
        ('Venta', 'Venta'),
        ('Devolución', 'Devolución'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    tipo_movimiento = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO_CHOICES)
    motivo = models.CharField(max_length=50, choices=MOTIVO_CHOICES)
    cantidad = models.IntegerField()
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True, help_text="Detalles adicionales del movimiento")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.tipo_movimiento} de {self.cantidad} unidades de {self.producto.nombre}"

    class Meta:
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"
        ordering = ['-fecha_movimiento']
