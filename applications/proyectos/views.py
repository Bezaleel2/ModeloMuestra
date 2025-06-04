from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# from django.contrib.auth.decorators import login_required # Si necesitas proteger la vista
from .models import Obra
from .forms import ObraForm

# @login_required # Descomenta si es necesario
def agregar_obra(request):
    if request.method == 'POST':
        form = ObraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Obra agregada exitosamente!')
            return redirect('proyectos:lista_obras') # Redirigir a la lista de obras (crearemos esta URL después)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else: # Si es un GET request
        form = ObraForm()

    context = {
        'form': form,
        'titulo_pagina': 'Agregar Nueva Obra'
    }
    return render(request, 'proyectos/agregar_obra.html', context)

# @login_required # Descomenta si es necesario
def lista_obras(request):
    obras = Obra.objects.all()
    context = {
        'obras': obras,
        'titulo_pagina': 'Listado de Obras'
    }
    # Asegúrate de crear el template 'proyectos/lista_obras.html'
    return render(request, 'proyectos/lista_obras.html', context)

# Puedes añadir vistas para editar y eliminar más adelante
# def editar_obra(request, pk):
#     obra = get_object_or_404(Obra, pk=pk)
#     if request.method == 'POST':
#         form = ObraForm(request.POST, instance=obra)
#         if form.is_valid():
#             form.save()
#             messages.success(request, '¡Obra actualizada exitosamente!')
#             return redirect('proyectos:lista_obras')
#     else:
#         form = ObraForm(instance=obra)
#     context = {'form': form, 'titulo_pagina': 'Editar Obra'}
#     return render(request, 'proyectos/agregar_obra.html', context) # Reutilizamos el template

# def eliminar_obra(request, pk):
#     obra = get_object_or_404(Obra, pk=pk)
#     if request.method == 'POST': # Solo si se confirma la eliminación
#         obra.delete()
#         messages.success(request, '¡Obra eliminada exitosamente!')
#         return redirect('proyectos:lista_obras')
#     # Aquí podrías renderizar una página de confirmación antes de eliminar
#     context = {'obra': obra, 'titulo_pagina': 'Confirmar Eliminación'}
#     return render(request, 'proyectos/confirmar_eliminar_obra.html', context)