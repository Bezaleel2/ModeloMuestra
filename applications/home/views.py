from django.shortcuts import render

# Create your views here.

def login_view(request):
    return render(request, 'home/login.html')

def inicio_view(request):
    return render(request, 'home/pantalla_inicio.html')