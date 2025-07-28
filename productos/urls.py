# productos/urls.py
from django.urls import path
from . import views

app_name = 'productos' # Define un namespace para esta aplicación (lo usaremos más adelante)

urlpatterns = [
   path('', views.lista_productos, name='lista_productos'),  # Ruta para listar productos
   path('<int:pk>/', views.detalle_producto, name='detalle_producto'),
   path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'), # Nueva URL para añadir al carrito
   path('carrito/', views.view_cart, name='view_cart'),
   path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
   path('update_cart_item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),

]