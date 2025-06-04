from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction, models
from applications.administracion.models import Pedido, PedidoItem
from applications.almacen.models import Producto
from .forms import SurtirItemFormSet

# @login_required
@transaction.atomic
def surtir_pedido_vista(request, pk):
    pedido_a_surtir = get_object_or_404(Pedido, pk=pk)
    
    # Prevenir surtir pedidos ya completados o cancelados
    if pedido_a_surtir.estado in ['COMPLETADO', 'CANCELADO']:
        messages.warning(request, f"El Pedido #{pedido_a_surtir.id} está '{pedido_a_surtir.get_estado_display()}' y no se puede modificar.")
        return redirect('operativo:lista_pedidos_surtir')

    if request.method == 'POST':
        formset = SurtirItemFormSet(request.POST, instance=pedido_a_surtir, prefix='items')

        if formset.is_valid():
            stock_suficiente_para_todo = True
            items_con_cantidad_a_surtir = []

            for form_item in formset:
                if form_item.is_valid() and form_item.cleaned_data:
                    cantidad_a_surtir_ahora = form_item.cleaned_data.get('cantidad_a_surtir_ahora', 0)
                    
                    if cantidad_a_surtir_ahora > 0:
                        pedido_item_actual = form_item.instance
                        try:
                            producto_en_almacen = Producto.objects.select_for_update().get(pk=pedido_item_actual.producto.pk)
                        except Producto.DoesNotExist:
                            form_item.add_error(None, f"Producto '{pedido_item_actual.producto.nombre_producto}' no encontrado en almacén.")
                            stock_suficiente_para_todo = False
                            continue # Siguiente item del formset

                        if producto_en_almacen.cantidad < cantidad_a_surtir_ahora:
                            form_item.add_error('cantidad_a_surtir_ahora', 
                                f"Stock insuficiente para '{producto_en_almacen.nombre_producto}'. Disp: {producto_en_almacen.cantidad}, Sol: {cantidad_a_surtir_ahora}")
                            stock_suficiente_para_todo = False
                        else:
                            items_con_cantidad_a_surtir.append({
                                'pedido_item': pedido_item_actual,
                                'producto_almacen': producto_en_almacen,
                                'cantidad_surtir_ahora': cantidad_a_surtir_ahora
                            })
            
            if not stock_suficiente_para_todo or not formset.is_valid():
                messages.error(request, "No se pudo procesar el surtido. Verifica el stock o las cantidades.")
            else:
                if not items_con_cantidad_a_surtir:
                    messages.info(request, "No se especificaron cantidades para surtir en ningún ítem.")
                else:
                    for item_data in items_con_cantidad_a_surtir:
                        pedido_item = item_data['pedido_item']
                        producto_almacen = item_data['producto_almacen']
                        cantidad_surtir_ahora = item_data['cantidad_surtir_ahora']

                        pedido_item.cantidad_surtida += cantidad_surtir_ahora
                        pedido_item.save(update_fields=['cantidad_surtida'])

                        producto_almacen.cantidad = models.F('cantidad') - cantidad_surtir_ahora
                        producto_almacen.save(update_fields=['cantidad'])
                    
                    messages.success(request, f"Surtido para el Pedido #{pedido_a_surtir.id} procesado.")

                # Actualizar el estado general del Pedido después de procesar todos los ítems
                pedido_a_surtir.actualizar_estado_segun_items()
                
                return redirect('operativo:lista_pedidos_surtir')
        else:
            messages.error(request, "Por favor corrige los errores en las cantidades a surtir.")
    else: # GET
        formset = SurtirItemFormSet(instance=pedido_a_surtir, prefix='items')

    context = {
        'pedido': pedido_a_surtir,
        'item_formset': formset,
        'titulo_pagina': f"Surtir Pedido #{pedido_a_surtir.id}"
    }
    return render(request, 'operativo/surtir_pedido_form.html', context)

# ... (lista_pedidos_para_surtir se mantiene igual, pero ahora mostrará el estado) ...
def lista_pedidos_para_surtir(request):
    pedidos = Pedido.objects.all().order_by('fecha_pedido').prefetch_related('items', 'items__producto')
    context = {
        'pedidos': pedidos,
        'titulo_pagina': 'Lista de Pedidos para Surtir'
    }
    return render(request, 'operativo/lista_pedidos_surtir.html', context)