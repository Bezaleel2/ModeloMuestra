from .base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

DATABASES = {
    'default': {
        # Configuración por defecto, por ejemplo para SQLite si DATABASE_URL no está definida
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASE_URL_ENV = os.environ.get('DATABASE_URL')
if DATABASE_URL_ENV:
    print(f"DEBUG: Encontrada DATABASE_URL del entorno: {DATABASE_URL_ENV[:30]}...") # Para depurar que sí la lee
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL_ENV)
else:
    print("DEBUG: NO se encontró DATABASE_URL del entorno, usando default de SQLite.")

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
