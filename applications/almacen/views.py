from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm # Asumimos que ProductoForm ya está definido
from django.shortcuts import get_object_or_404

# @login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid(): # ModelForm validará la unicidad de nombre_producto aquí
            form.save()
            messages.success(request, f'Producto "{form.cleaned_data["nombre_producto"]}" agregado exitosamente al inventario.')
            return redirect('almacen:lista_productos')
        else:
            # Si el form no es válido (ej. nombre duplicado, u otros errores),
            # se volverá a renderizar el template con el form que contiene los errores.
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else: # GET
        form = ProductoForm()

    context = {
        'form': form,
        'titulo_pagina': 'Agregar Nuevo Producto al Almacén'
    }
    return render(request, 'almacen/agregar_producto.html', context)

def editar_producto(request, pk):
    producto_a_editar = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto_a_editar)
        if form.is_valid(): # Con el clean_nombre_producto en forms.py, esto debería funcionar
            
            instancia_guardada = form.save(commit=False) # No guarda en BD todavía. Contiene los datos actualizados del form (nombre, OC, proveedor).

            cantidad_agregada = form.cleaned_data.get('cantidad_a_agregar') # Obtiene el valor limpio
            if cantidad_agregada is not None and cantidad_agregada > 0:
                instancia_guardada.cantidad = producto_a_editar.cantidad + cantidad_agregada

            if cantidad_agregada is not None and cantidad_agregada > 0:
                instancia_guardada.cantidad += cantidad_agregada
            
            instancia_guardada.save()
            messages.success(request, f'Producto "{instancia_guardada.nombre_producto}" actualizado exitosamente.')
            if cantidad_agregada is not None and cantidad_agregada > 0:
                messages.info(request, f'Se agregaron {cantidad_agregada} unidades al stock. Nueva cantidad total: {instancia_guardada.cantidad}')
            return redirect('almacen:lista_productos')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ProductoForm(instance=producto_a_editar)
    context = {
        'form': form,
        'producto': producto_a_editar,
        'titulo_pagina': f'Editar Producto: {producto_a_editar.nombre_producto}'
    }
    return render(request, 'almacen/editar_producto.html', context)
def lista_productos(request):
    """
    Vista para mostrar el listado de todos los productos en el almacén.
    """
    productos = Producto.objects.all().order_by('nombre_producto')
    context = {
        'productos': productos,
        'titulo_pagina': 'Inventario de Almacén' 
    }
    return render(request, 'almacen/lista_productos.html', context)

def eliminar_producto(request, pk):
    producto_a_eliminar = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        # Si el formulario de confirmación se envía (método POST), eliminamos el producto.
        nombre_producto_eliminado = producto_a_eliminar.nombre_producto # Guardamos el nombre para el mensaje
        producto_a_eliminar.delete()
        messages.success(request, f'Producto "{nombre_producto_eliminado}" eliminado exitosamente del inventario.')
        return redirect('almacen:lista_productos')
    
    # Si es una solicitud GET, mostramos la página de confirmación.
    context = {
        'producto': producto_a_eliminar,
        'titulo_pagina': f'Confirmar Eliminación: {producto_a_eliminar.nombre_producto}'
    }
    return render(request, 'almacen/confirmar_eliminar_producto.html', context)