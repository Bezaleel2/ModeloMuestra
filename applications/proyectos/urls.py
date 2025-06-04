from django.urls import path
from . import views

app_name = 'proyectos'  # Define el namespace de la aplicación

urlpatterns = [
    path('agregar/', views.agregar_obra, name='agregar_obra'),
    path('lista/', views.lista_obras, name='lista_obras'),
    # path('editar/<int:pk>/', views.editar_obra, name='editar_obra'),
    # path('eliminar/<int:pk>/', views.eliminar_obra, name='eliminar_obra'),
]