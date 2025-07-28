# productos/context_processors.py
from .models import CarritoItem

def cart_item_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        # Suma las cantidades de todos los items en el carrito del usuario
        cart_count = CarritoItem.objects.filter(usuario=request.user).count() # o .aggregate(Sum('cantidad'))['cantidad__sum'] si quieres sumar las cantidades
    return {'cart_count': cart_count}


#Nota: He puesto .count() para contar el número de tipos diferentes de productos en el carrito. Si quieres sumar las cantidades totales de todos los productos (ej. 3 manzanas + 2 peras = 5 items en total), cambia count() por:
#from django.db.models import Sum
#cart_count = CarritoItem.objects.filter(usuario=request.user).aggregate(Sum('cantidad'))['cantidad__sum'] or 0