
from django.urls import path
from . import views
from core.views import CustomLoginView # Importa la vista de login que creaste

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    
     
]