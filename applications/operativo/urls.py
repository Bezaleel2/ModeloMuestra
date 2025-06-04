from django.urls import path
from . import views

app_name = 'operativo'

urlpatterns = [
    path('pedidos-para-surtir/', views.lista_pedidos_para_surtir, name='lista_pedidos_surtir'),
    # DESCOMENTA O AÑADE ESTA LÍNEA:
    path('surtir-pedido/<int:pk>/', views.surtir_pedido_vista, name='surtir_pedido_accion'),
]