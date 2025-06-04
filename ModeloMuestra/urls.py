"""
URL configuration for ModeloMuestra project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from applications.usuariosdjango.views import login_vista, logout_vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_vista, name='login'),
    path('logout/', logout_vista, name='logout'),
    #apps
    path('', include("applications.home.urls")),
    path('usuariosdjango/', include('applications.usuariosdjango.urls')),
    path('', include('applications.proyectos.urls')),
    path('proveedores/', include('applications.proveedores.urls')),
    path('almacen/', include('applications.almacen.urls')),
    path('administracion/', include('applications.administracion.urls')),
    path('operativo/', include('applications.operativo.urls')),
]