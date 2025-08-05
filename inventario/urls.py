# inventario/urls.py
from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.historial_movimientos, name='historial_movimientos'),
    path('crear/', views.crear_movimiento, name='crear_movimiento'),
    path('descargar-pdf/', views.descargar_historial_pdf, name='descargar_historial_pdf'),
]
