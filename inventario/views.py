# inventario/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.paginator import Paginator
from io import BytesIO
from xhtml2pdf import pisa
from productos.models import Producto
from .models import MovimientoInventario

# Decorador para restringir el acceso solo a usuarios staff (administradores)
def is_admin(user):
    return user.is_staff

# Función auxiliar para convertir HTML a PDF
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

@login_required
@user_passes_test(is_admin)
def historial_movimientos(request):
    movimientos_list = MovimientoInventario.objects.all()
    paginator = Paginator(movimientos_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj
    }
    return render(request, 'inventario/historial_movimientos.html', context)

@login_required
@user_passes_test(is_admin)
def crear_movimiento(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        tipo_movimiento = request.POST.get('tipo_movimiento')
        motivo = request.POST.get('motivo')
        cantidad = int(request.POST.get('cantidad', 0))
        descripcion = request.POST.get('descripcion')
        
        try:
            with transaction.atomic():
                producto = Producto.objects.get(pk=producto_id)
                
                if tipo_movimiento == 'Entrada':
                    producto.stock += cantidad
                    producto.save()
                    MovimientoInventario.objects.create(
                        producto=producto,
                        tipo_movimiento=tipo_movimiento,
                        motivo=motivo,
                        cantidad=cantidad,
                        descripcion=descripcion,
                        usuario=request.user
                    )
                    messages.success(request, f"Se han agregado {cantidad} unidades de {producto.nombre} al stock.")
                
                elif tipo_movimiento == 'Salida':
                    if producto.stock >= cantidad:
                        producto.stock -= cantidad
                        producto.save()
                        MovimientoInventario.objects.create(
                            producto=producto,
                            tipo_movimiento=tipo_movimiento,
                            motivo=motivo,
                            cantidad=cantidad,
                            descripcion=descripcion,
                            usuario=request.user
                        )
                        messages.success(request, f"Se han retirado {cantidad} unidades de {producto.nombre} del stock.")
                    else:
                        messages.error(request, f"Error: No hay suficiente stock de {producto.nombre} para realizar esta salida.")
                        return redirect('inventario:crear_movimiento')
        except Producto.DoesNotExist:
            messages.error(request, "El producto seleccionado no existe.")
        except ValueError:
            messages.error(request, "La cantidad debe ser un número válido.")
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado: {e}")
            
        return redirect('inventario:historial_movimientos')
        
    productos = Producto.objects.all().order_by('nombre')
    context = {
        'productos': productos,
        'motivos_entrada': ['Compra a proveedor'],
        'motivos_salida': ['Novedad (daño, pérdida)', 'Devolución'],
    }
    return render(request, 'inventario/crear_movimiento.html', context)

@login_required
@user_passes_test(is_admin)
def descargar_historial_pdf(request):
    movimientos = MovimientoInventario.objects.all()
    context = {'movimientos': movimientos}
    pdf = render_to_pdf('inventario/historial_movimientos_pdf.html', context)
    
    if pdf:
        response = pdf
        response['Content-Disposition'] = f'attachment; filename="historial_inventario.pdf"'
        return response
        
    return HttpResponse("Ocurrió un error al generar el PDF del historial.", status=500)
