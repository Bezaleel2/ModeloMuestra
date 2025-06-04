from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required # Opcional, si quieres que solo usuarios logueados vean la lista
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import CustomUser # ¡Importa tu modelo CustomUser!
from django.contrib import messages

def register_request(request):
    """
    Vista para el registro de nuevos usuarios.
    Maneja el envío del formulario de registro.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Registro exitoso! Has iniciado sesión.")
            return redirect("usuariosdjango:lista_usuarios") # Redirige a la página de inicio o a donde quieras
        else:
            # Si el formulario no es válido, los errores se mostrarán en la plantilla
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuariosdjango/agregar_usuario.html', {'form': form})

def login_request(request):
    """
    Vista para el inicio de sesión de usuarios.
    Maneja el envío del formulario de inicio de sesión.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"¡Hola {username}! Has iniciado sesión.")
                return redirect("home") # Redirige a la página de inicio
            else:
                messages.error(request,"Nombre de usuario o contraseña inválidos.")
        else:
            messages.error(request,"Nombre de usuario o contraseña inválidos.")
    form = AuthenticationForm()
    return render(request, "registration/login.html", {"login_form": form})

def logout_request(request):
    """
    Vista para cerrar la sesión del usuario.
    """
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect("home") # Redirige a la página de inicio o a la de login

def lista_usuarios(request):
    """
    Vista para mostrar la lista de todos los usuarios registrados.
    """
    usuarios = CustomUser.objects.all().order_by('username') # Obtiene todos los usuarios, ordenados por username
    context = {
        'usuarios': usuarios,
        'titulo_pagina': 'Lista de Usuarios Registrados' # Un título opcional para tu template
    }
    return render(request, 'usuariosdjango/lista_usuarios.html', context)


def login_vista(request): # Nuevo nombre o asegúrate que es el que usas
    if request.user.is_authenticated:
        # Si el usuario ya está autenticado, redirigirlo a la página de inicio
        return redirect('pantalla_inicio') # Asumiendo que tienes una URL con name='inicio'

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Bienvenido de nuevo, {username}.")
                # Redirigir a la página de inicio después del login exitoso
                # Es mejor usar un nombre de URL si 'inicio' lo tiene, sino la ruta directa.
                return redirect('/inicio/') # O redirect('nombre_url_inicio')
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    else: # GET request
        form = AuthenticationForm()
    
    context = {
        'form': form,
        'titulo_pagina': 'Iniciar Sesión' # Para el <title> de tu HTML
    }
    return render(request, 'home/login.html', context) # Asegúrate que tu template se llama login.html

def logout_vista(request):
    """
    Cierra la sesión del usuario actual.
    """
    if request.user.is_authenticated: # Solo cerrar sesión si hay una sesión activa
        logout(request)
        messages.info(request, "Has cerrado sesión exitosamente.")
    # Redirigir a la página de login o a la de inicio, según prefieras
    # Usar el nombre de la URL es más robusto
    return redirect('login') # O 'inicio' si prefieres que vaya a la página principal pública