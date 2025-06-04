from django.urls import path
from . import views

app_name = 'almacen'

urlpatterns = [
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('producto/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
]