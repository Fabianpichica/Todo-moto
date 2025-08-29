# core/views.py

from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from productos.models import Producto   # Asegúrate de que esta línea esté presente y correcta.
from productos.views import _merge_carts 
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings

def landing_page(request):
        productos_recuperados = Producto.objects.filter(disponible=True).order_by('-fecha_creacion')[:6]
        
        print(f"\n--- DEBUG DE PRODUCTOS PARA LANDING PAGE ---")
        print(f"Número de productos recuperados: {productos_recuperados.count()}")
        if productos_recuperados.exists():
            for p in productos_recuperados:
                print(f"  ID: {p.id}, Nombre: {p.nombre}, Precio: {p.precio}, Stock: {p.stock}, Disponible: {p.disponible}, Imagen: {p.imagen}")
        else:
            print("  No se encontraron productos disponibles en la base de datos.")
        print(f"--- FIN DEBUG ---")
        
        context = {
            'productos': productos_recuperados,
            'product_name': 'Producto Estrella del Emprendimiento',
            'product_description': 'Descubre nuestro increíble producto, diseñado para mejorar tu día a día con innovación y calidad. ¡No te lo pierdas!',
            'product_image_url': 'https://via.placeholder.com/400x300?text=Tu+Producto+Aqui',
        }
        return render(request, 'core/landing_page.html', context)

def enviar_correo_bienvenida(email, nombre):
    from django.core.mail import send_mail
    from django.conf import settings
    subject = '¡Bienvenido a Raberbike!'
    message = f'Hola {nombre},\n\nGracias por registrarte en Raberbike. Tu cuenta ha sido creada exitosamente.\n\n¡Disfruta de nuestros productos y servicios!\n\nEl equipo de Raberbike.'
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )

def register(request):
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                # ¡LLAMADA A LA FUNCIÓN DE FUSIÓN DESPUÉS DE REGISTRARSE E INICIAR SESIÓN!
                _merge_carts(request, user) 
                # Enviar correo de bienvenida tras registro exitoso
                enviar_correo_bienvenida(user.email, user.first_name or user.username)
                return redirect('landing_page')
        else:
            form = CustomUserCreationForm()
        return render(request, 'core/register.html', {'form': form})

    # ¡ASEGÚRATE DE QUE ESTA CLASE ESTÉ DEFINIDA ASÍ EN core/views.py!
class CustomLoginView(LoginView):
        template_name = 'core/login.html'

        def form_valid(self, form):
            """
            Se llama cuando los datos del formulario de login son válidos.
            Aquí es donde se inicia sesión al usuario y luego se fusiona el carrito.
            """
            response = super().form_valid(form) # Llama al método original de LoginView para iniciar sesión
            # ¡LLAMADA A LA FUNCIÓN DE FUSIÓN DESPUÉS DE INICIAR SESIÓN!
            _merge_carts(self.request, self.request.user)
            return response

    # Vista para cerrar sesión
def custom_logout(request):
        logout(request)
        return redirect('landing_page')

def detalle_producto(request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        context = {
            'producto': producto
        }
        return render(request, 'productos/detalle_producto.html', context)

def nosotros(request):
    return render(request, 'core/nosotros.html')

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        cuerpo = f"Nombre: {nombre}\nCorreo: {email}\nMensaje: {mensaje}"
        send_mail(
            'Nuevo mensaje de contacto Raber Biker',
            cuerpo,
            settings.DEFAULT_FROM_EMAIL,
            ['raberbikes@gmail.com'], # Correo de destino corregido
            fail_silently=False,
        )
        return render(request, 'core/contacto.html', {'enviado': True})
    return render(request, 'core/contacto.html')