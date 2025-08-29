from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from productos.models import Producto 
from .models import Categoria 
from .forms import CategoriaForm, ProductoForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from productos.models import Pedido, PedidoItem
from collections import defaultdict
from django.db.models import Sum, Q
from django.db.models.functions import ExtractMonth 
import json
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.views.decorators.http import require_POST

# Función auxiliar para verificar si el usuario es staff (administrador)
def is_staff(user):
    return user.is_staff

@login_required # Requiere que el usuario esté logueado
@user_passes_test(is_staff) # Requiere que el usuario sea staff (administrador)
def dashboard_home(request):
    # Vista principal del dashboard
    return render(request, 'dashboard_admin/dashboard_home.html')

# Vistas de CRUD para Productos
# Vistas de CRUD para Productos (¡ACTUALIZADAS AHORA!)
@login_required
@user_passes_test(is_staff)
def producto_list(request):
    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'dashboard_admin/producto_list.html', {'productos': productos})

@login_required
@user_passes_test(is_staff)
def producto_create(request):
    """
    Permite crear un nuevo producto.
    """
    if request.method == 'POST':
        # request.FILES es necesario para manejar la subida de imágenes
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('dashboard_admin:producto_list')
        else:
            messages.error(request, "Error al crear el producto. Por favor, revisa los campos.")
    else:
        form = ProductoForm()
    return render(request, 'dashboard_admin/producto_form.html', {'form': form, 'action': 'create'})

@login_required
@user_passes_test(is_staff)
def producto_update(request, pk):
    """
    Permite editar un producto existente.
    """
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        # instance=producto carga los datos existentes del producto en el formulario
        # request.FILES es necesario para manejar la subida de imágenes
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f"Producto '{producto.nombre}' actualizado correctamente.")
            return redirect('dashboard_admin:producto_list')
        else:
            messages.error(request, "Error al actualizar el producto. Por favor, revisa los campos.")
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'dashboard_admin/producto_form.html', {'form': form, 'producto': producto, 'action': 'update'})

@login_required
@user_passes_test(is_staff)
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, f"Producto '{producto.nombre}' eliminado correctamente.")
    return redirect('dashboard_admin:producto_list') # Redirigir a la lista después de eliminar

# Vistas de CRUD para Categorías (esbozos, la implementaremos después de crear el modelo)
# Vistas de CRUD para Categorías (¡IMPLEMENTADAS AHORA!)
@login_required
@user_passes_test(is_staff)
def categoria_list(request):
    """
    Muestra una lista de todas las categorías.
    """
    categorias = Categoria.objects.all().order_by('nombre')  # Mostrar todas, no solo activas
    return render(request, 'dashboard_admin/categoria_list.html', {'categorias': categorias})

@login_required
@user_passes_test(is_staff)
def categoria_create(request):
    """
    Permite crear una nueva categoría.
    """
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada correctamente.")
            return redirect('dashboard_admin:categoria_list')
        else:
            messages.error(request, "Error al crear la categoría. Por favor, revisa los campos.")
    else:
        form = CategoriaForm()
    return render(request, 'dashboard_admin/categoria_form.html', {'form': form, 'action': 'create'})

@login_required
@user_passes_test(is_staff)
def categoria_update(request, pk):
    """
    Permite editar una categoría existente.
    """
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, f"Categoría '{categoria.nombre}' actualizada correctamente.")
            return redirect('dashboard_admin:categoria_list')
        else:
            messages.error(request, "Error al actualizar la categoría. Por favor, revisa los campos.")
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'dashboard_admin/categoria_form.html', {'form': form, 'categoria': categoria, 'action': 'update'})

@login_required
@user_passes_test(is_staff)
def categoria_delete(request, pk):
    """
    Permite eliminar una categoría.
    """
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, f"Categoría '{categoria.nombre}' eliminada correctamente.")
    return redirect('dashboard_admin:categoria_list')

@login_required
@user_passes_test(is_staff)
def desactivar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.activa = False
        categoria.save()
        messages.success(request, f"La categoría '{categoria.nombre}' ha sido desactivada.")
    return redirect('dashboard_admin:categoria_list')

@login_required
@user_passes_test(is_staff)
def activar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.activa = True
        categoria.save()
        messages.success(request, f"La categoría '{categoria.nombre}' ha sido activada.")
    return redirect('dashboard_admin:categoria_list')

# ¡NUEVA VISTA para ver todos los pedidos de los clientes!
@login_required
@user_passes_test(is_staff)
def ver_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha_creacion')
    paginator = Paginator(pedidos, 10) # 10 pedidos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj
    }
    return render(request, 'dashboard_admin/ver_pedidos.html', context)

# ¡NUEVA VISTA para ver todos los clientes!
@login_required
@user_passes_test(is_staff)
def ver_clientes(request):
    # Excluye a los usuarios que son staff (para no listarse a sí mismo como cliente)
    clientes = User.objects.filter(is_staff=False).order_by('username')
    paginator = Paginator(clientes, 10) # 10 clientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'dashboard_admin/ver_clientes.html', context)

# ¡NUEVA VISTA para el panel de reportes!
@login_required
@user_passes_test(is_staff)
def dashboard_reportes(request):
    # Obtener pedidos completados para las métricas de ventas
    pedidos_completados = Pedido.objects.filter(estado='Completado')
    
    # Calcular métricas generales
    total_pedidos = Pedido.objects.all().count()
    total_clientes = User.objects.filter(is_staff=False).count()
    total_ingresos = sum(p.total_pedido for p in pedidos_completados)
    
    # Calcular los productos más vendidos para el gráfico
    productos_vendidos_count = defaultdict(int)
    for item in PedidoItem.objects.all():
        productos_vendidos_count[item.producto.nombre] += item.cantidad
        
    productos_vendidos_ordenados = sorted(
        productos_vendidos_count.items(), 
        key=lambda item: item[1], 
        reverse=True
    )[:5] # Obtener los 5 productos más vendidos

    # Preparar datos para el gráfico de productos
    productos_labels = [item[0] for item in productos_vendidos_ordenados]
    productos_data = [item[1] for item in productos_vendidos_ordenados]
    
    # Calcular los ingresos por mes para el gráfico
    pedidos_por_mes = pedidos_completados.annotate(month=ExtractMonth('fecha_creacion')).values('month').annotate(total=Sum('total_pedido')).order_by('month')
    
    meses_mapping = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
        7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    ventas_mensuales_labels = [meses_mapping.get(item['month']) for item in pedidos_por_mes]
    ventas_mensuales_data = [float(item['total']) for item in pedidos_por_mes]
    
    context = {
        'total_pedidos': total_pedidos,
        'total_clientes': total_clientes,
        'total_ingresos': total_ingresos,
        'productos_labels': json.dumps(productos_labels),
        'productos_data': json.dumps(productos_data),
        'ventas_mensuales_labels': json.dumps(ventas_mensuales_labels),
        'ventas_mensuales_data': json.dumps(ventas_mensuales_data),
    }
    return render(request, 'dashboard_admin/dashboard_reportes.html', context)

# Función auxiliar para convertir HTML a PDF
def render_to_pdf(template_src, context_dict={}):
    """Convierte una plantilla HTML a un archivo PDF."""
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# NUEVA VISTA: Descargar factura
@login_required
def descargar_factura(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Verificación de seguridad: solo el administrador o el dueño del pedido pueden descargar la factura
    if not request.user.is_staff and pedido.usuario != request.user:
        return HttpResponseForbidden("No tienes permiso para descargar esta factura.")

    subtotal = float(pedido.total_pedido)
    iva = subtotal * 0.19
    total = subtotal + iva

    # Renderiza la plantilla HTML a PDF
    pdf = render_to_pdf('dashboard_admin/factura_pdf.html', {
        'pedido': pedido,
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
    })

    if pdf:
        response = pdf
        # Con 'attachment', el navegador fuerza la descarga del archivo
        response['Content-Disposition'] = f'attachment; filename="factura_pedido_{pedido.id}.pdf"'
        return response

    return HttpResponse("Ocurrió un error al generar la factura.", status=500)

@login_required
@user_passes_test(is_staff)
@require_POST
def cambiar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    nuevo_estado = request.POST.get('nuevo_estado')
    # Solo permitir los estados válidos
    ESTADOS_VALIDOS = ['Pendiente', 'En camino', 'Entregado', 'Completado', 'Cancelado']
    if nuevo_estado in ESTADOS_VALIDOS:
        pedido.estado = nuevo_estado
        pedido.save()
        messages.success(request, f"El estado del pedido #{pedido.pk} ha sido actualizado a '{nuevo_estado}'.")
    else:
        messages.error(request, "Estado no válido.")
    return redirect('dashboard_admin:ver_pedidos')
