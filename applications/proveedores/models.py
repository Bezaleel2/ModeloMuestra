from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Proveedor")
    direccion = models.TextField(verbose_name="Dirección", blank=True, null=True)
    telefono = models.CharField(max_length=20, verbose_name="Teléfono", blank=True, null=True)
    credito = models.BooleanField(default=False, verbose_name="¿Ofrece Crédito?") # True para "Sí", False para "No"

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre']