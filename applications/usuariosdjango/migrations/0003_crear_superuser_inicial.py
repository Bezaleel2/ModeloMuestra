# applications/usuariosdjango/migrations/000X_crear_superuser_inicial.py
from django.db import migrations
from django.contrib.auth.hashers import make_password # Para crear contraseñas de forma segura
import os # Para leer variables de entorno (opcional pero recomendado)

def crear_superuser(apps, schema_editor):
    """
    Crea un superusuario si no existe.
    Lee las credenciales de variables de entorno o usa valores por defecto.
    ¡CAMBIA LA CONTRASEÑA INMEDIATAMENTE DESPUÉS DEL PRIMER LOGIN!
    """
    User = apps.get_model('usuariosdjango', 'CustomUser') # Usa tu app_label y nombre de modelo CustomUser

    # Es MEJOR usar variables de entorno para las credenciales en producción
    # En Render, configurarías estas variables de entorno.
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin_deploy')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Bezaleel') # ¡CAMBIAR ESTA CONTRASEÑA!

    if not User.objects.filter(username=username).exists():
        print(f"Creando superusuario inicial: {username} con email {email}")
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            # Puedes añadir aquí los campos adicionales de tu CustomUser si son obligatorios
            # y no tienen un valor por defecto en el modelo.
            # nombre="Admin", 
            # apellidos="Principal",
        )
    else:
        print(f"Superusuario '{username}' ya existe. No se crea de nuevo.")

class Migration(migrations.Migration):
    dependencies = [
        ('usuariosdjango', '000Y_previous_migration'), # Asegúrate que esta sea tu última migración de usuariosdjango
    ]
    operations = [
        migrations.RunPython(crear_superuser),
    ]