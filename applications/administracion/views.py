from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction, models # Importamos transaction y models para F()
# from django.contrib.auth.decorators import login_required

from .models import Pedido, PedidoItem
from .forms import PedidoForm, PedidoItemFormSet
from applications.almacen.models import Producto # Para acceder al stock

# @login_required
@transaction.atomic # Envuelve toda la función en una transacción de base de datos
def agregar_pedido(request):
    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST, prefix='pedido')
        # Pasamos request.POST también al formset para validarlo
        item_formset = PedidoItemFormSet(request.POST, prefix='items')

        if pedido_form.is_valid() and item_formset.is_valid():
            # --- INICIO DE LÓGICA DE STOCK Y GUARDADO ---
            
            # Paso 1: Verificar stock para todos los ítems antes de hacer cualquier cambio
            stock_suficiente_para_todo = True
            items_para_procesar = [] # Guardaremos (producto_db, cantidad_pedida)

            for item_form_cleaned_data in item_formset.cleaned_data:
                # cleaned_data es una lista de diccionarios. Saltamos los vacíos o marcados para borrar.
                if not item_form_cleaned_data or item_form_cleaned_data.get('DELETE'):
                    continue

                producto_solicitado = item_form_cleaned_data.get('producto')
                cantidad_pedida = item_form_cleaned_data.get('cantidad')

                if not producto_solicitado or cantidad_pedida is None or cantidad_pedida <= 0:
                    # Esto debería ser manejado por la validación del PedidoItemForm (min_value=1 para cantidad)
                    # pero es una doble verificación.
                    messages.error(request, "Hay un problema con la cantidad o el producto en uno de los ítems.")
                    stock_suficiente_para_todo = False
                    break
                
                # Obtenemos la instancia actual del producto desde la BD para verificar stock real
                try:
                    # Usamos select_for_update() para bloquear la fila del producto si esperamos alta concurrencia,
                    # previniendo que otro proceso modifique el stock mientras verificamos y actualizamos.
                    # Para la mayoría de los casos, .get() es suficiente si la transacción es corta.
                    producto_en_almacen = Producto.objects.get(pk=producto_solicitado.pk)
                except Producto.DoesNotExist:
                    messages.error(request, f"El producto '{producto_solicitado.nombre_producto}' ya no existe en el almacén.")
                    stock_suficiente_para_todo = False
                    break

                if producto_en_almacen.cantidad < cantidad_pedida:
                    messages.error(request, f"Stock insuficiente para '{producto_en_almacen.nombre_producto}'. Disponible: {producto_en_almacen.cantidad}, Solicitado: {cantidad_pedida}.")
                    stock_suficiente_para_todo = False
                    break # No es necesario seguir verificando si uno falla
                
                items_para_procesar.append({
                    'producto_db': producto_en_almacen, # La instancia con el stock actual
                    'cantidad_pedida': cantidad_pedida,
                    'form_data': item_form_cleaned_data # Guardamos los datos del form del ítem
                })

            if stock_suficiente_para_todo:
                # Paso 2: Si hay stock para todo, guardamos el pedido
                pedido = pedido_form.save(commit=False)
                # Aquí podrías asignar el usuario actual si es necesario:
                # if request.user.is_authenticated:
                #     pedido.algun_campo_de_usuario = request.user
                pedido.save() # Guardamos el objeto Pedido

                # Paso 3: Creamos los PedidoItem y descontamos el stock
                for item_info in items_para_procesar:
                    producto_db = item_info['producto_db']
                    cantidad_pedida = item_info['cantidad_pedida']
                    
                    # Creamos el PedidoItem
                    PedidoItem.objects.create(
                        pedido=pedido,
                        producto=producto_db, # Usamos la instancia que ya teníamos
                        cantidad_pedida=cantidad_pedida
                    )
                    
                    # Descontamos el stock de forma atómica (segura para concurrencia)
                    producto_db.cantidad = models.F('cantidad') - cantidad_pedida
                    producto_db.save(update_fields=['cantidad']) # Solo actualiza el campo cantidad
                    # OJO: Después de .save() con F(), producto_db.cantidad en memoria no se actualiza,
                    # si necesitas el valor nuevo, haz producto_db.refresh_from_db()

                messages.success(request, f'Pedido ID: {pedido.id} creado exitosamente y stock actualizado.')
                return redirect('administracion:lista_pedidos')
            else:
                # Si no hay stock suficiente, los mensajes de error ya se agregaron.
                # Simplemente se volverá a renderizar el formulario con los datos ingresados y los errores.
                # La transacción se revertirá porque no llegamos a un redirect exitoso.
                pass
            # --- FIN DE LÓGICA DE STOCK Y GUARDADO ---
        else: # pedido_form o item_formset no son válidos por otras razones
            if not pedido_form.is_valid():
                messages.error(request, 'Por favor corrige los errores en los datos generales del pedido.')
            if not item_formset.is_valid():
                messages.error(request, 'Por favor corrige los errores en los ítems del pedido.')
                # Para depurar errores del formset:
                # for form_in_formset_errors in item_formset.errors:
                #     if form_in_formset_errors: # Si el diccionario de errores no está vacío
                #         for field, field_errors in form_in_formset_errors.items():
                #             messages.warning(request, f"Error en ítem ({field}): {', '.join(field_errors)}")
                # if item_formset.non_form_errors():
                #    messages.warning(request, f"Errores generales en ítems: {item_formset.non_form_errors()}")


    else: # GET
        pedido_form = PedidoForm(prefix='pedido')
        # Para el GET, es importante pasar queryset=PedidoItem.objects.none() al formset
        # si no quieres que intente cargar ítems relacionados con una instancia no existente de Pedido.
        item_formset = PedidoItemFormSet(prefix='items', queryset=PedidoItem.objects.none())

    context = {
        'pedido_form': pedido_form,
        'item_formset': item_formset,
        'titulo_pagina': 'Agregar Nuevo Pedido'
    }
    return render(request, 'administracion/agregar_pedido.html', context)

# Tu vista lista_pedidos se mantiene igual
def lista_pedidos(request):
    pedidos = Pedido.objects.all().prefetch_related('items', 'items__producto')
    context = {
        'pedidos': pedidos,
        'titulo_pagina': 'Listado de Pedidos'
    }
    return render(request, 'administracion/lista_pedidos.html', context)

def eliminar_pedido(request, pk):
    pedido_a_eliminar = get_object_or_404(Pedido, pk=pk)

    if request.method == 'POST':
        # Si el formulario de confirmación se envía (método POST), eliminamos el pedido.
        # Los PedidoItem se eliminarán en cascada si así se definió en el modelo (on_delete=models.CASCADE)
        id_pedido_eliminado = pedido_a_eliminar.id # Guardamos el ID para el mensaje
        pedido_a_eliminar.delete()
        messages.success(request, f'Pedido ID: #{id_pedido_eliminado} eliminado exitosamente.')
        return redirect('administracion:lista_pedidos')
    
    # Si es una solicitud GET, mostramos la página de confirmación.
    context = {
        'pedido': pedido_a_eliminar,
        'titulo_pagina': f'Confirmar Eliminación del Pedido #{pedido_a_eliminar.id}'
    }
    return render(request, 'administracion/confirmar_eliminar_pedido.html', context)

def detalle_pedido(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.prefetch_related('items__producto'),
        pk=pk
    )
    context = {
        'pedido': pedido,
        'titulo_pagina': f'Detalles del Pedido #{pedido.id}'
    }
    return render(request, 'administracion/detalle_pedido.html', context)