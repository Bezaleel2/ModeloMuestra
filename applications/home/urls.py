from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('inicio/', views.inicio_view, name='pantalla_inicio'),
]