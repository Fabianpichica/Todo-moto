# productos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# from django.contrib.auth.decorators import login_required # ¡Ya no lo necesitamos para ninguna vista de carrito!
from django.db.models import Sum
from .models import Producto, CarritoItem, Pedido, PedidoItem
from django.urls import reverse # Para usar reverse en get_absolute_url si lo necesitas
from django.http import JsonResponse # Añade esta línea
from django.db import transaction
from dashboard_admin.models import Categoria 
from django.db.models import Sum, Q
from django.contrib.auth.decorators import login_required
from .models import Producto, Categoria, Perfil, Pedido, PedidoItem
from inventario.models import MovimientoInventario
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

COLOMBIAN_CITIES = [
    'Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena',
    'Cúcuta', 'Bucaramanga', 'Pereira', 'Santa Marta', 'Manizales',
    'Ibagué', 'Soledad', 'Villavicencio', 'Neiva', 'Valledupar',
    # Añade más ciudades según sea necesario
]

# Función auxiliar para obtener el identificador del carrito (usuario o session_key)
def _get_or_create_cart_identifier(request):
    if request.user.is_authenticated:
        return {'usuario': request.user, 'session_key': None}
    else:
        # Asegúrate de que la sesión exista y tenga una clave
        if not request.session.session_key:
            request.session.save() # Forzar la creación de una session_key si no existe
        return {'usuario': None, 'session_key': request.session.session_key}
    
# NUEVA FUNCIÓN: Lógica para fusionar carritos al iniciar sesión/registrarse
def _merge_carts(request, user):
        session_key = request.session.session_key
        if not session_key:
            return # No hay sesión para fusionar

        # Obtener ítems del carrito asociados a la sesión actual
        session_cart_items = CarritoItem.objects.filter(session_key=session_key, usuario__isnull=True)

        if session_cart_items.exists():
            with transaction.atomic(): # Usamos una transacción para asegurar que todo se guarde o nada
                for session_item in session_cart_items:
                    # Intentar encontrar un CarritoItem existente para este usuario y producto
                    user_cart_item, created = CarritoItem.objects.get_or_create(
                        usuario=user,
                        producto=session_item.producto,
                        defaults={'cantidad': session_item.cantidad, 'session_key': None} # Si es nuevo, asigna cantidad y limpia session_key
                    )

                    if not created:
                        # Si el producto ya estaba en el carrito del usuario, actualiza la cantidad
                        user_cart_item.cantidad += session_item.cantidad
                        user_cart_item.save()
                    
                    # Eliminar el CarritoItem original de la sesión
                    session_item.delete()
            
            # Limpiar la session_key de la sesión de Django para evitar futuras confusiones
            # Esto es opcional, pero ayuda a asegurar que no se sigan asociando ítems a una sesión "vacía"
            # request.session['session_key'] = None # No es necesario si se borran los items, pero es una opción.
            messages.info(request, "Los ítems de tu carrito anónimo han sido fusionados con tu cuenta.")




def lista_productos(request, category_id=None):
    # Obtener la consulta de búsqueda de los parámetros GET
    query = request.GET.get('q')

    # Obtener todos los productos disponibles
    productos = Producto.objects.filter(disponible=True)

    # Si se proporciona un category_id, filtrar por esa categoría
    if category_id:
        productos = productos.filter(categoria__id=category_id)
    
    # Si se proporciona una consulta de búsqueda, filtrar por nombre o descripción
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        ).distinct() # Usamos distinct para evitar duplicados si un producto coincide en ambos campos

    # Ordenar los productos (por ejemplo, por fecha de creación descendente)
    productos = productos.order_by('-fecha_creacion')

    # Obtener todas las categorías para mostrarlas en el filtro
    categorias = Categoria.objects.all().order_by('nombre')

    context = {
        'productos': productos,
        'categorias': categorias, # Pasamos todas las categorías al contexto
        'selected_category_id': category_id, # Pasamos el ID de la categoría seleccionada (si hay una)
        'query': query # Pasamos el término de búsqueda al contexto para mostrarlo en la barra
    }
    return render(request, 'productos/lista_productos.html', context)

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    context = {
        'producto': producto
    }
    return render(request, 'productos/detalle_producto.html', context)

# add_to_cart ahora devuelve JSON
def add_to_cart(request, pk):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, pk=pk)
        
        try:
            cantidad = int(request.POST.get('cantidad', 1))
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Cantidad no válida.'}, status=400)

        if cantidad <= 0:
            return JsonResponse({'success': False, 'message': "La cantidad debe ser al menos 1."}, status=400)

        identifier = _get_or_create_cart_identifier(request)
        print(f"\n--- DEBUG add_to_cart ---")
        print(f"Identifier: {identifier}")
        print(f"Adding {cantidad} of product {producto.nombre} (ID: {pk})")

        try:
            with transaction.atomic(): # Asegura la atomicidad para get_or_create y update
                if identifier['usuario']: # Usuario logueado
                    carrito_item, created = CarritoItem.objects.get_or_create(
                        usuario=identifier['usuario'],
                        producto=producto,
                        defaults={'cantidad': cantidad}
                    )
                else: # Usuario anónimo (usando session_key)
                    carrito_item, created = CarritoItem.objects.get_or_create(
                        session_key=identifier['session_key'],
                        producto=producto,
                        defaults={'cantidad': cantidad}
                    )

                print(f"CarritoItem created: {created}")
                if not created:
                    # Si el item ya existía, incrementa la cantidad
                    carrito_item.cantidad += cantidad
                    carrito_item.save()
                    message = f"Se han añadido {cantidad} unidades adicionales de '{producto.nombre}' al carrito."
                else:
                    message = f"'{producto.nombre}' ha sido añadido al carrito."
                
                print(f"CarritoItem quantity after operation: {carrito_item.cantidad}")

                # Calcula el total de ítems en el carrito DESPUÉS de que el ítem actual ha sido procesado y guardado
                cart_total_items = 0
                if identifier['usuario']:
                    cart_total_items = CarritoItem.objects.filter(usuario=identifier['usuario']).aggregate(total=Sum('cantidad'))['total'] or 0
                else:
                    cart_total_items = CarritoItem.objects.filter(session_key=identifier['session_key']).aggregate(total=Sum('cantidad'))['total'] or 0
                
                print(f"Calculated cart_total_items to send: {cart_total_items}")
                print(f"--- END DEBUG add_to_cart ---\n")

                return JsonResponse({'success': True, 'message': message, 'cart_total_items': cart_total_items})

        except Exception as e:
            print(f"--- ERROR add_to_cart ---")
            print(f"Exception: {str(e)}")
            print(f"--- END ERROR add_to_cart ---\n")
            return JsonResponse({'success': False, 'message': f"Ocurrió un error: {str(e)}"}, status=500)
    else:
        return JsonResponse({'success': False, 'message': "Método no permitido para añadir al carrito."}, status=405)


# ¡Eliminado! Ahora cualquiera puede ver su carrito
def view_cart(request):
    identifier = _get_or_create_cart_identifier(request)
    
    if identifier['usuario']: # Usuario logueado
        carrito_items = CarritoItem.objects.filter(usuario=identifier['usuario']).select_related('producto')
    else: # Usuario anónimo
        carrito_items = CarritoItem.objects.filter(session_key=identifier['session_key']).select_related('producto')
    
    total_carrito = sum(item.get_total_item_price() for item in carrito_items)
    
    context = {
        'carrito_items': carrito_items,
        'total_carrito': total_carrito,
    }
    return render(request, 'productos/carrito.html', context)

# ¡Eliminado!
def remove_from_cart(request, item_id):
    identifier = _get_or_create_cart_identifier(request)
    
    if identifier['usuario']: # Usuario logueado
        carrito_item = get_object_or_404(CarritoItem, id=item_id, usuario=identifier['usuario'])
    else: # Usuario anónimo
        carrito_item = get_object_or_404(CarritoItem, id=item_id, session_key=identifier['session_key'])

    if request.method == 'POST':
        carrito_item.delete()
        messages.success(request, f"'{carrito_item.producto.nombre}' ha sido eliminado del carrito.")
    else:
        messages.error(request, "Método no permitido para eliminar del carrito.")

    return redirect('productos:view_cart')

# ¡Eliminado!
def update_cart_item(request, item_id):
    identifier = _get_or_create_cart_identifier(request)
    
    if identifier['usuario']: # Usuario logueado
        carrito_item = get_object_or_404(CarritoItem, id=item_id, usuario=identifier['usuario'])
    else: # Usuario anónimo
        carrito_item = get_object_or_404(CarritoItem, id=item_id, session_key=identifier['session_key'])

    if request.method == 'POST':
        try:
            nueva_cantidad = int(request.POST.get('cantidad'))
        except (ValueError, TypeError):
            messages.error(request, "Cantidad no válida.")
            return redirect('productos:view_cart')

        if nueva_cantidad <= 0:
            carrito_item.delete()
            messages.info(request, f"'{carrito_item.producto.nombre}' ha sido eliminado del carrito.")
        elif nueva_cantidad > carrito_item.producto.stock:
            messages.error(request, f"No hay suficiente stock para '{carrito_item.producto.nombre}'. Stock disponible: {carrito_item.producto.stock}.")
        else:
            carrito_item.cantidad = nueva_cantidad
            carrito_item.save()
            messages.success(request, f"Cantidad de '{carrito_item.producto.nombre}' actualizada a {nueva_cantidad}.")
    else:
        messages.error(request, "Método no permitido para actualizar el carrito.")

    return redirect('productos:view_cart')

# NUEVA VISTA: Para obtener el total de ítems del carrito (vía AJAX)
def get_cart_total_items(request):
    identifier = _get_or_create_cart_identifier(request)
    cart_total_items = 0
    if identifier['usuario']:
        cart_total_items = CarritoItem.objects.filter(usuario=identifier['usuario']).aggregate(total=Sum('cantidad'))['total'] or 0
    else:
        cart_total_items = CarritoItem.objects.filter(session_key=identifier['session_key']).aggregate(total=Sum('cantidad'))['total'] or 0
    
    return JsonResponse({'success': True, 'cart_total_items': cart_total_items})



def checkout(request):
    identifier = _get_or_create_cart_identifier(request)
    if identifier['usuario']:
        carrito_items = CarritoItem.objects.filter(usuario=identifier['usuario']).select_related('producto')
        first_name = identifier['usuario'].first_name
        last_name = identifier['usuario'].last_name
        email = identifier['usuario'].email
    else:
        carrito_items = CarritoItem.objects.filter(session_key=identifier['session_key']).select_related('producto')
        first_name = last_name = email = ''

    if not carrito_items.exists():
        messages.warning(request, "Tu carrito está vacío. Añade productos para continuar.")
        return redirect('productos:lista_productos')

    subtotal = sum(item.get_total_item_price() for item in carrito_items)
    iva = (subtotal * Decimal('0.19')).quantize(Decimal('0.01'))  # IVA del 19%
    total_carrito = (subtotal + iva).quantize(Decimal('0.01'))

    context = {
        'carrito_items': carrito_items,
        'subtotal': subtotal,
        'iva': iva,
        'total_carrito': total_carrito,
        'ciudades': COLOMBIAN_CITIES,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
    }
    return render(request, 'productos/checkout.html', context)


def process_checkout(request):
    if request.method == 'POST':
        identifier = _get_or_create_cart_identifier(request)
        if identifier['usuario']:
            carrito_items = CarritoItem.objects.filter(usuario=identifier['usuario']).select_related('producto')
            nombre_completo = request.POST.get('nombre_completo', '').strip()
            email = request.POST.get('email', '').strip()
            direccion = request.POST.get('direccion', '').strip()
            ciudad = request.POST.get('ciudad', '').strip()
            metodo_pago = request.POST.get('metodo_pago', '').strip()
            telefono = ''
            tipo_documento = ''
            numero_documento = ''
        else:
            carrito_items = CarritoItem.objects.filter(session_key=identifier['session_key']).select_related('producto')
            nombre_completo = request.POST.get('nombre_completo', '').strip()
            email = request.POST.get('email', '').strip()
            telefono = request.POST.get('telefono', '').strip()
            tipo_documento = request.POST.get('tipo_documento', '').strip()
            numero_documento = request.POST.get('numero_documento', '').strip()
            direccion = request.POST.get('direccion', '').strip()
            ciudad = request.POST.get('ciudad', '').strip()
            metodo_pago = request.POST.get('metodo_pago', '').strip()
        total_pedido = sum(item.get_total_item_price() for item in carrito_items)
        # Validar email de usuario anónimo
        if not identifier['usuario']:
            from django.core.validators import validate_email
            from django.core.exceptions import ValidationError
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, "El correo electrónico ingresado no es válido.")
                return redirect('productos:checkout')
        try:
            with transaction.atomic():
                pedido = Pedido.objects.create(
                    usuario=identifier['usuario'],
                    nombre=nombre_completo,
                    direccion=direccion,
                    ciudad=ciudad,
                    total_pedido=total_pedido,
                )
                for item in carrito_items:
                    PedidoItem.objects.create(
                        pedido=pedido,
                        producto=item.producto,
                        cantidad=item.cantidad,
                        precio_unitario=item.producto.precio
                    )
                carrito_items.delete()
                # Enviar correo de confirmación/factura al usuario anónimo
                if not identifier['usuario']:
                    subject = 'Factura de tu compra en MotoGM'
                    factura_html = render_to_string('productos/email_factura.html', {
                        'pedido': pedido,
                        'pedido_items': pedido.items.all(),
                        'nombre': nombre_completo,
                        'email': email,
                        'telefono': telefono,
                        'tipo_documento': tipo_documento,
                        'numero_documento': numero_documento,
                        'direccion': direccion,
                        'ciudad': ciudad,
                        'metodo_pago': metodo_pago,
                        'total_pedido': total_pedido,
                    })
                    send_mail(
                        subject,
                        '',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        html_message=factura_html,
                        fail_silently=False
                    )
            messages.success(request, "¡Tu pedido ha sido procesado correctamente!")
            return redirect('productos:lista_productos')
        except Exception as e:
            messages.error(request, f"Ocurrió un error al procesar el pedido: {str(e)}")
            return redirect('productos:checkout')
    else:
        return redirect('productos:checkout')


def mis_pedidos(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para ver tus pedidos.")
        return redirect('core:login')
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    context = {
        'pedidos': pedidos
    }
    return render(request, 'productos/mis_pedidos.html', context)


def mi_cuenta(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para acceder a tu cuenta.")
        return redirect('core:login')
    perfil, created = Perfil.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Lógica para actualizar la información de contacto
        if 'update_info' in request.POST:
            request.user.username = request.POST.get('username')
            request.user.email = request.POST.get('email')
            try:
                request.user.save()
                messages.success(request, 'Tu información de contacto ha sido actualizada exitosamente.')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al actualizar tu información: {e}')
            return redirect('productos:mi_cuenta')
            
        # Lógica para actualizar la dirección de envío
        elif 'update_address' in request.POST:
            perfil.direccion = request.POST.get('direccion')
            perfil.ciudad = request.POST.get('ciudad')
            perfil.codigo_postal = request.POST.get('codigo_postal')
            perfil.pais = request.POST.get('pais')
            try:
                perfil.save()
                messages.success(request, 'Tu dirección de envío ha sido actualizada exitosamente.')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al actualizar tu dirección: {e}')
            return redirect('productos:mi_cuenta')
            
    context = {
        'perfil': perfil
    }
    return render(request, 'productos/mi_cuenta.html', context)


def checkout_view(request):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        if not carrito:
            messages.error(request, "Tu carrito está vacío.")
            return redirect('productos:ver_carrito')
        
        # Asume que el total ya está calculado en la sesión
        total_pedido = sum(item['precio'] * item['cantidad'] for item in carrito.values())
        
        try:
            with transaction.atomic():
                # Creación del pedido con los campos obligatorios. 
                # Los campos opcionales (dirección, etc.) se dejarán vacíos.
                pedido = Pedido.objects.create(
                    cliente=request.user,
                    total_pedido=total_pedido,
                    # Si tu formulario tiene estos campos, los puedes agregar aquí:
                    # nombre=request.POST.get('nombre'),
                    # direccion_envio=request.POST.get('direccion_envio'),
                    # ciudad=request.POST.get('ciudad'),
                    # codigo_postal=request.POST.get('codigo_postal'),
                    # pais=request.POST.get('pais')
                )

                for item_data in carrito.values():
                    producto = Producto.objects.get(id=item_data['id'])
                    cantidad = item_data['cantidad']
                    
                    if producto.stock >= cantidad:
                        # Resta el stock del producto
                        producto.stock -= cantidad
                        producto.save()
                        
                        # CREA UN REGISTRO DE MOVIMIENTO DE INVENTARIO
                        MovimientoInventario.objects.create(
                            producto=producto,
                            tipo_movimiento='Salida',
                            motivo='Venta',
                            cantidad=cantidad,
                            descripcion=f"Venta en línea - Pedido #{pedido.id}",
                            usuario=request.user
                        )
                        
                        PedidoItem.objects.create(
                            pedido=pedido,
                            producto=producto,
                            cantidad=cantidad,
                            precio=item_data['precio']
                        )
                    else:
                        raise ValueError(f"No hay suficiente stock para {producto.nombre}.")
                
                del request.session['carrito']
                messages.success(request, '¡Tu pedido ha sido realizado con éxito!')
                return redirect('productos:mis_pedidos')

        except Producto.DoesNotExist:
            messages.error(request, "Uno de los productos en tu carrito no existe.")
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"Ocurrió un error al procesar tu pedido: {e}")
            
    # Si tuvieras un formulario en esta vista, iría aquí
    return render(request, 'productos/checkout.html', {})
