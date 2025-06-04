from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
    path('agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('lista/', views.lista_proveedores, name='lista_proveedores'),
    # Aquí podrías añadir URLs para editar, eliminar, etc. en el futuro
]