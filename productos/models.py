# productos/models.py
from django.db import models
from django.contrib.auth.models import User 

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True) # Las imágenes se guardarán en media/productos/
    stock = models.IntegerField(default=0)
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre'] # Ordena los productos por nombre por defecto

class CarritoItem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) # Un item pertenece a un usuario
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) # Un item está asociado a un producto
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} de {self.usuario.username}"

    def get_total_item_price(self):
        return self.cantidad * self.producto.precio

    class Meta:
        # Esto asegura que un usuario no pueda tener el mismo producto dos veces en el carrito,
        # en su lugar, se incrementaría la cantidad.
        unique_together = ('usuario', 'producto')