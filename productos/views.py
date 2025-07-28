from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Producto, CarritoItem


def lista_productos(request):
    # Obtener todos los productos de la base de datos
    productos = Producto.objects.all()
    # Pasar los productos al contexto para que puedan ser mostrados en la plantilla
    context = {
        'productos': productos
    }
    # Renderizar el template 'lista_productos.html' con los productos
    return render(request, 'productos/lista_productos.html', context)

def detalle_producto(request, pk):
    # Obtener un solo producto por su clave primaria (pk)
    producto = Producto.objects.get(pk=pk)
    # Pasar el producto al contexto
    context = {
        'producto': producto
    }
    # Renderizar el template 'detalle_producto.html' con el producto
    return render(request, 'productos/detalle_producto.html', context)


@login_required # Solo usuarios logueados pueden añadir al carrito
def add_to_cart(request, pk):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, pk=pk)
        cantidad = int(request.POST.get('cantidad', 1)) # Obtiene la cantidad del formulario, por defecto 1

        # Asegúrate de que la cantidad no sea negativa o cero
        if cantidad <= 0:
            messages.error(request, "La cantidad debe ser al menos 1.")
            return redirect('productos:detalle_producto', pk=pk) # O a la landing page

        # Verifica si el producto ya está en el carrito del usuario
        carrito_item, created = CarritoItem.objects.get_or_create(
            usuario=request.user,
            producto=producto,
            defaults={'cantidad': cantidad} # Si es nuevo, establece la cantidad
        )

        if not created:
            # Si el item ya existía, incrementa la cantidad
            carrito_item.cantidad += cantidad
            carrito_item.save()
            messages.success(request, f"Se han añadido {cantidad} unidades adicionales de '{producto.nombre}' al carrito.")
        else:
            messages.success(request, f"'{producto.nombre}' ha sido añadido al carrito.")

        # Redirige a la página de donde vino el usuario o a una página de confirmación
        return redirect('landing_page') # Redirige a la landing page, puedes cambiarlo a donde quieras
    else:
        messages.error(request, "Método no permitido para añadir al carrito.")
        return redirect('landing_page')
    
    
@login_required
def view_cart(request):
    # Recupera todos los CarritoItems para el usuario logueado
    # .select_related('producto') optimiza la consulta para obtener los datos del producto
    carrito_items = CarritoItem.objects.filter(usuario=request.user).select_related('producto')
    
    # Calcula el total del carrito
    total_carrito = 0
    if carrito_items.exists():
        for item in carrito_items:
            total_carrito += item.get_total_item_price() # Asegúrate de que CarritoItem tenga este método
    
    context = {
        'carrito_items': carrito_items,
        'total_carrito': total_carrito,
    }
    return render(request, 'productos/carrito.html', context)


#vista para eliminar productos en nuestro carrito de compras
@login_required
def remove_from_cart(request, item_id):
    # Asegúrate de que solo el propietario del CarritoItem pueda eliminarlo
    carrito_item = get_object_or_404(CarritoItem, id=item_id, usuario=request.user)

    if request.method == 'POST':
        carrito_item.delete()
        messages.success(request, f"'{carrito_item.producto.nombre}' ha sido eliminado del carrito.")
    else:
        messages.error(request, "Método no permitido para eliminar del carrito.")

    return redirect('productos:view_cart') # Redirige de nuevo a la vista del carrito



#vista para actualizar cantidades en nuestro carrito de compras:

@login_required
def update_cart_item(request, item_id):
    carrito_item = get_object_or_404(CarritoItem, id=item_id, usuario=request.user)

    if request.method == 'POST':
        try:
            # Obtiene la nueva cantidad del formulario (asegurando que sea un entero)
            nueva_cantidad = int(request.POST.get('cantidad'))
        except (ValueError, TypeError):
            messages.error(request, "Cantidad no válida.")
            return redirect('productos:view_cart')

        if nueva_cantidad <= 0:
            # Si la cantidad es 0 o menos, elimina el item del carrito
            carrito_item.delete()
            messages.info(request, f"'{carrito_item.producto.nombre}' ha sido eliminado del carrito.")
        elif nueva_cantidad > carrito_item.producto.stock:
            messages.error(request, f"No hay suficiente stock para '{carrito_item.producto.nombre}'. Stock disponible: {carrito_item.producto.stock}.")
        else:
            # Actualiza la cantidad y guarda
            carrito_item.cantidad = nueva_cantidad
            carrito_item.save()
            messages.success(request, f"Cantidad de '{carrito_item.producto.nombre}' actualizada a {nueva_cantidad}.")
    else:
        messages.error(request, "Método no permitido para actualizar el carrito.")

    return redirect('productos:view_cart') # Siempre redirige de nuevo a la vista del carrito
    



