# applications/usuariosdjango/migrations/0003_crear_superuser_inicial.py
from django.db import migrations
from django.contrib.auth.hashers import make_password
import os

def crear_superuser(apps, schema_editor):
    User = apps.get_model('usuariosdjango', 'CustomUser')
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin_deploy')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'ContraseñaSegura123')
    if not User.objects.filter(username=username).exists():
        print(f"Creando superusuario inicial: {username} con email {email}")
        User.objects.create_superuser(
            username=username, email=email, password=password
        )
    else:
        print(f"Superusuario '{username}' ya existe. No se crea de nuevo.")

class Migration(migrations.Migration):
    dependencies = [
        ('usuariosdjango', '0001_initial'), # <--- CORREGIDO (o el nombre de tu última migración)
    ]
    operations = [
        migrations.RunPython(crear_superuser),
    ]