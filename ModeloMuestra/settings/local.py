# ModeloMuestra/settings/local.py
from .base import * # Importa todas las configuraciones base

# --- CONFIGURACIONES ESPECÍFICAS DE DESARROLLO LOCAL ---

# DEBUG: Siempre True en desarrollo local (sobrescribe el default de base.py si DJANGO_DEBUG no está en .env)
DEBUG = True

# SECRET_KEY:
# base.py ya intenta cargar DJANGO_SECRET_KEY desde .env.
# Si quieres una clave específica solo para local y diferente a la de .env,
# puedes definirla aquí, pero usualmente .env es suficiente.
# Ejemplo: SECRET_KEY = 'mi_clave_local_super_secreta_diferente_a_la_de_env'

# ALLOWED_HOSTS: Para desarrollo local
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# DATABASE:
# La configuración de base.py ya maneja DATABASE_URL desde .env.
# Si no tienes DATABASE_URL en tu .env, usará el default de SQLite de base.py.
# No necesitas redefinir DATABASES aquí a menos que quieras forzar algo diferente
# a lo que .env o el default de base.py provean.

# STATICFILES_STORAGE:
# Para desarrollo con DEBUG=True, el servidor de desarrollo de Django sirve los estáticos.
# Si usas `whitenoise.runserver_nostatic` en INSTALLED_APPS (como está en base.py),
# WhiteNoise los servirá. No necesitas `CompressedManifestStaticFilesStorage` aquí.

# Configuración de Email para desarrollo (imprimir a consola)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Opcional: Django Debug Toolbar (si la usas)
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
# INTERNAL_IPS = ['127.0.0.1']