    # dashboard_admin/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from productos.models import Producto # Importamos Producto para gestionarlo
from.forms import ProductoForm

    # Función auxiliar para verificar si el usuario es staff (administrador)
def is_staff(user):
        return user.is_staff
@login_required # Requiere que el usuario esté logueado
@user_passes_test(is_staff) # Requiere que el usuario sea staff (administrador)
def dashboard_home(request):
        # Vista principal del dashboard
        return render(request, 'dashboard_admin/dashboard_home.html')

    # Vistas de CRUD para Productos
@login_required
@user_passes_test(is_staff)
def producto_list(request):
        productos = Producto.objects.all().order_by('nombre')
        return render(request, 'dashboard_admin/producto_list.html', {'productos': productos})

@login_required
@user_passes_test(is_staff)
def producto_create(request):
        # Lógica para crear un producto (usaremos un formulario de Django más adelante)
        return render(request, 'dashboard_admin/producto_form.html') # Usaremos la misma plantilla para crear/editar

@login_required
@user_passes_test(is_staff)
def producto_update(request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        # Lógica para actualizar un producto (usaremos un formulario de Django más adelante)
        return render(request, 'dashboard_admin/producto_form.html', {'producto': producto})

@login_required
@user_passes_test(is_staff)
def producto_delete(request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        if request.method == 'POST':
            producto.delete()
            messages.success(request, f"Producto '{producto.nombre}' eliminado correctamente.")
        return redirect('dashboard_admin:producto_list') # Redirigir a la lista después de eliminar

    # Vistas de CRUD para Categorías (esbozos, la implementaremos después de crear el modelo)
@login_required
@user_passes_test(is_staff)
def categoria_list(request):
        # Categoría no existe aún, solo un placeholder
        categorias = [] # Placeholder
        messages.info(request, "La gestión de categorías se implementará una vez que tengamos el modelo de Categoría.")
        return render(request, 'dashboard_admin/categoria_list.html', {'categorias': categorias})

@login_required
@user_passes_test(is_staff)
def categoria_create(request):
        return render(request, 'dashboard_admin/categoria_form.html')

@login_required
@user_passes_test(is_staff)
def categoria_update(request, pk):
        # Necesitarás un modelo de Categoría para esto
        return render(request, 'dashboard_admin/categoria_form.html')

@login_required
@user_passes_test(is_staff)
def categoria_delete(request, pk):
        # Necesitarás un modelo de Categoría para esto
        messages.error(request, "La función de eliminar categoría aún no está implementada.")
        return redirect('dashboard_admin:categoria_list')

@login_required
@user_passes_test(is_staff)
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado exitosamente.")
            return redirect('dashboard_admin:producto_list')
    else:
        form = ProductoForm()
    return render(request, 'dashboard_admin/producto_form.html', {'form': form})
