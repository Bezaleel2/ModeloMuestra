from django.db import models
from django.utils import timezone
from applications.almacen.models import Producto

class Pedido(models.Model):
    nombre_creador = models.CharField(
        max_length=150,
        verbose_name="Nombre de quien crea el pedido"
    )
    fecha_pedido = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha del Pedido"
    )
    # --- ESTE CAMPO ES ESENCIAL ---
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('SURTIDO_PARCIAL', 'Surtido Parcialmente'),
        ('COMPLETADO', 'Completado'), # Anteriormente 'Finalizado', 'COMPLETADO' es más estándar
        ('CANCELADO', 'Cancelado'),
    ]
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='PENDIENTE',
        verbose_name="Estado del Pedido"
    )
    # --- FIN DEL CAMPO ESTADO ---

    def __str__(self):
        return f"Pedido ID: {self.id} - Creado por: {self.nombre_creador} el {self.fecha_pedido.strftime('%d/%m/%Y %H:%M')}"

    def actualizar_estado_segun_items(self):
        """
        Actualiza el estado del pedido basado en las cantidades surtidas de sus ítems.
        Llama a este método después de modificar la cantidad_surtida de un PedidoItem.
        """
        if not self.items.exists(): # Si no tiene ítems, podría ser un error o un pedido vacío
            self.estado = 'PENDIENTE' # O algún otro estado inicial
            self.save()
            return

        total_items = self.items.count()
        items_completamente_surtidos = 0
        items_parcialmente_surtidos = 0

        for item in self.items.all():
            if item.cantidad_surtida >= item.cantidad_pedida:
                items_completamente_surtidos += 1
            elif item.cantidad_surtida > 0:
                items_parcialmente_surtidos += 1
        
        if items_completamente_surtidos == total_items:
            self.estado = 'COMPLETADO'
        elif items_completamente_surtidos > 0 or items_parcialmente_surtidos > 0:
            self.estado = 'SURTIDO_PARCIAL'
        else: # Ningún ítem ha sido surtido (o todos tienen cantidad_surtida = 0)
            self.estado = 'PENDIENTE'
        self.save(update_fields=['estado'])


    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_pedido']

# ... tu modelo PedidoItem se mantiene igual ...
class PedidoItem(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        related_name='items',
        on_delete=models.CASCADE
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        verbose_name="Producto del Almacén"
    )
    cantidad_pedida = models.PositiveIntegerField(verbose_name="Cantidad Pedida")
    cantidad_surtida = models.PositiveIntegerField(
        verbose_name="Cantidad Ya Surtida",
        default=0
    )

    @property
    def cantidad_pendiente(self):
        return self.cantidad_pedida - self.cantidad_surtida

    def __str__(self):
        return f"{self.cantidad_pedida} x {self.producto.nombre_producto} (Surtido: {self.cantidad_surtida}) (Pedido: {self.pedido.id})"

    class Meta:
        verbose_name = "Ítem de Pedido"
        verbose_name_plural = "Ítems de Pedido"
        unique_together = ('pedido', 'producto')