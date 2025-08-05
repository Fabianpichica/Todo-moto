from django.urls import path, include
from . import views

app_name = 'dashboard_admin' # Namespace para esta app

urlpatterns = [
        path('', views.dashboard_home, name='dashboard_home'),
        # URLs para Productos
        path('productos/', views.producto_list, name='producto_list'),
        path('productos/crear/', views.producto_create, name='producto_create'),
        path('productos/<int:pk>/editar/', views.producto_update, name='producto_update'),
        path('productos/<int:pk>/eliminar/', views.producto_delete, name='producto_delete'),

        # URLs para Categorías (crearemos el modelo de Categoría más adelante)
        path('categorias/', views.categoria_list, name='categoria_list'),
        path('categorias/crear/', views.categoria_create, name='categoria_create'),
        path('categorias/<int:pk>/editar/', views.categoria_update, name='categoria_update'),
        path('categorias/<int:pk>/eliminar/', views.categoria_delete, name='categoria_delete'),


        path('ver-pedidos/', views.ver_pedidos, name='ver_pedidos'),

        path('ver-clientes/', views.ver_clientes, name='ver_clientes'),

        path('reportes/', views.dashboard_reportes, name='dashboard_reportes'),

        path('pedidos/<int:pedido_id>/descargar-factura/', views.descargar_factura, name='descargar_factura'),

        path('inventario/', include('inventario.urls')),
]
    
    