from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    nombre = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=150, blank=True, null=True, verbose_name="Apellidos")
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

    # Métodos existentes
    def is_administrativo(self):
        return self.groups.filter(name='Administrativo').exists()

    def is_operativo(self):
        return self.groups.filter(name='Operativo').exists()

    # --- NUEVOS MÉTODOS PARA NUEVOS ROLES ---
    def is_jefe_de_piso(self):
        return self.groups.filter(name='Jefe de piso').exists()

    def is_admin_secundario(self):
        return self.groups.filter(name='Administrador secundario').exists()
    # --- FIN DE NUEVOS MÉTODOS ---