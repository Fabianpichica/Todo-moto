from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from productos.models import Producto # Importamos Producto para gestionarlo
from .models import Categoria # Importamos el nuevo modelo Categoria
from .forms import CategoriaForm, ProductoForm# Importamos el nuevo formulario CategoriaForm


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
        categorias = Categoria.objects.all().order_by('nombre')
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
    