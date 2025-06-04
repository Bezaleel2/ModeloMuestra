# applications/almacen/models.py
from django.db import models
from applications.proveedores.models import Proveedor

class Producto(models.Model):
    numero_orden_compra = models.CharField(
        max_length=50,
        verbose_name="Número de Orden de Compra",
        blank=True,
        null=True
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Proveedor"
    )
    nombre_producto = models.CharField(
        max_length=200,
        verbose_name="Nombre del Producto",
        unique=True  # <--- ¡AÑADIR ESTO!
    )
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    # ... (otros campos si los tienes) ...

    def __str__(self):
        return self.nombre_producto

    class Meta:
        verbose_name = "Producto de Almacén"
        verbose_name_plural = "Productos de Almacén"
        ordering = ['nombre_producto']