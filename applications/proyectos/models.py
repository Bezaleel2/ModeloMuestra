from django.db import models
from django.utils import timezone # Para la fecha por defecto

class Obra(models.Model):
    nombre_obra = models.CharField(max_length=200, verbose_name="Nombre de la Obra")
    encargado_obra = models.CharField(max_length=150, verbose_name="Encargado de Obra")
    fecha_estimada_entrega = models.DateField(verbose_name="Fecha Estimada de Entrega", default=timezone.now)
    ubicacion = models.CharField(max_length=255, verbose_name="Ubicación", blank=True, null=True)
    # Podrías añadir más campos si los necesitas, por ejemplo:
    # descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    # fecha_creacion = models.DateTimeField(auto_now_add=True)
    # fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_obra

    class Meta:
        verbose_name = "Obra"
        verbose_name_plural = "Obras"
        ordering = ['-fecha_estimada_entrega', 'nombre_obra']