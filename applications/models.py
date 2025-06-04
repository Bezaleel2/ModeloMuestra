from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    nombre = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=150, blank=True, null=True, verbose_name="Apellidos")
    telefono = models.CharField(max_length=15, blank=True, null=True)
    # email = models.EmailField(unique=True) 

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username', 'nombre']

    def __str__(self):
        return self.username

    # --- NUEVOS MÉTODOS PARA VERIFICAR GRUPOS ---
    def is_administrativo(self):
        return self.groups.filter(name='Administrativo').exists()

    def is_operativo(self):
        return self.groups.filter(name='Operativo').exists()
    # --- FIN DE NUEVOS MÉTODOS ---