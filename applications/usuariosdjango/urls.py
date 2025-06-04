from django.urls import path
from . import views

app_name = 'usuariosdjango'

urlpatterns = [
    path("register/", views.register_request, name="agregar_usuario"),
    path("login/", views.login_request, name="login"),
    path('logout/', views.logout_vista, name='logout'),
    path('lista/', views.lista_usuarios, name='lista_usuarios'),
]