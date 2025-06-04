from django.urls import path
from . import views

app_name = 'administracion'

urlpatterns = [
    path('agregar/', views.agregar_pedido, name='agregar_pedido'),
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('eliminar/<int:pk>/', views.eliminar_pedido, name='eliminar_pedido'),
    path('detalle/<int:pk>/', views.detalle_pedido, name='detalle_pedido'),
    # URLs para editar, ver detalle, eliminar pedidos en el futuro
]