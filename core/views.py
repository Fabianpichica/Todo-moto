# core/views.py

from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from productos.models import Producto   # Asegúrate de que esta línea esté presente y correcta.

from .forms import CustomUserCreationForm

def landing_page(request):
    # **** ESTA ES LA LÍNEA CLAVE QUE FALTABA O SE ELIMINÓ ****
    # Recupera los productos de la base de datos que estén disponibles
    productos_recuperados = Producto.objects.filter(disponible=True).order_by('-fecha_creacion')[:6]
    # Puedes cambiar el [:6] si quieres mostrar más o menos productos.
    
    # --- INICIO DE LÍNEAS PARA DEPURACIÓN (MOVidas después de la asignación) ---
    print(f"\n--- DEBUG DE PRODUCTOS PARA LANDING PAGE ---")
    print(f"Número de productos recuperados: {productos_recuperados.count()}")
    if productos_recuperados.exists():
        for p in productos_recuperados:
            print(f"  ID: {p.id}, Nombre: {p.nombre}, Precio: {p.precio}, Stock: {p.stock}, Disponible: {p.disponible}, Imagen: {p.imagen}")
    else:
        print("  No se encontraron productos disponibles en la base de datos.")
    print(f"--- FIN DEBUG ---")
    
    context = {
        'productos': productos_recuperados, # <--- ¡IMPORTANTE! Pasa los productos al contexto con la clave 'productos'
        'product_name': 'Producto Estrella del Emprendimiento', # Estos son datos estáticos, puedes eliminarlos si solo quieres mostrar los dinámicos
        'product_description': 'Descubre nuestro increíble producto, diseñado para mejorar tu día a día con innovación y calidad. ¡No te lo pierdas!',
        'product_image_url': 'https://via.placeholder.com/400x300?text=Tu+Producto+Aqui', # Placeholder
    }
    return render(request, 'core/landing_page.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('landing_page')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

# ¡ASEGÚRATE DE QUE ESTA CLASE ESTÉ DEFINIDA ASÍ EN core/views.py!
class CustomLoginView(LoginView):
    template_name = 'core/login.html'

# Vista para cerrar sesión
def custom_logout(request):
    logout(request)
    return redirect('landing_page')

def detalle_producto(request, pk):
    # get_object_or_404 es un atajo de Django que intenta obtener un objeto
    # y si no lo encuentra, lanza un error 404 (Página no encontrada)
    producto = get_object_or_404(Producto, pk=pk)
    context = {
        'producto': producto
    }
    return render(request, 'productos/detalle_producto.html', context)