from django.shortcuts import render, redirect
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from .models import Proveedor
from .forms import ProveedorForm

# @login_required
def agregar_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Proveedor agregado exitosamente!')
            return redirect('proveedores:lista_proveedores') # Redirigir a la lista de proveedores
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else: # GET
        form = ProveedorForm()

    context = {
        'form': form,
        'titulo_pagina': 'Agregar Nuevo Proveedor'
    }
    return render(request, 'proveedores/agregar_proveedor.html', context)

# @login_required
def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    context = {
        'proveedores': proveedores,
        'titulo_pagina': 'Listado de Proveedores'
    }
    # Crea el template 'proveedores/lista_proveedores.html' para mostrar esta lista
    return render(request, 'proveedores/lista_proveedores.html', context)