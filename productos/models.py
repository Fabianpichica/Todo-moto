# productos/models.py
from django.db import models
from django.contrib.auth.models import User 
from dashboard_admin.models import Categoria # Importamos el modelo Categoria desde dashboard_admin
from django.db.models import Sum

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True) # Las imágenes se guardarán en media/productos/
    stock = models.IntegerField(default=0)
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre'] # Ordena los productos por nombre por defecto

class CarritoItem(models.Model):
        # El usuario puede ser nulo si el carrito es de un usuario anónimo
        usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
        # Nuevo campo para almacenar la clave de sesión para usuarios anónimos
        session_key = models.CharField(max_length=40, null=True, blank=True)
        producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
        cantidad = models.PositiveIntegerField(default=1)
        fecha_agregado = models.DateTimeField(auto_now_add=True)

        class Meta:
            # Añadir una restricción para asegurar unicidad:
            # Un usuario (o una sesión) solo puede tener un CarritoItem por producto.
            # Esto es importante para evitar duplicados y manejar las cantidades correctamente.
            unique_together = ('usuario', 'producto', 'session_key')
            # Nota: unique_together con null=True en usuario/session_key puede ser complicado.
            # La lógica en la vista manejará la unicidad para evitar duplicados.

        def __str__(self):
            if self.usuario:
                return f'{self.cantidad} de {self.producto.nombre} para {self.usuario.username}'
            else:
                return f'{self.cantidad} de {self.producto.nombre} (Sesión: {self.session_key[:5]}...)'

        def get_total_item_price(self):
            return self.cantidad * self.producto.precio
        


# Añade una tupla de opciones para los estados del pedido
ESTADO_CHOICES = (
    ('Pendiente', 'Pendiente'),
    ('Completado', 'Completado'),
    ('Cancelado', 'Cancelado'),
)

# Nuevo modelo para el pedido
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Pendiente')
    
    def __str__(self):
        return f"Pedido #{self.pk} - {self.nombre}"

# Nuevo modelo para los items de un pedido
class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"


    