# ModeloMuestra/settings/base.py
from pathlib import Path
import os
import dj_database_url # Asegúrate que esté en requirements.txt
from dotenv import load_dotenv

# Carga variables desde el archivo .env (principalmente para desarrollo local)
# En producción, las variables de entorno se establecen directamente en el servidor.
dotenv_path = Path(__file__).resolve().parent.parent.parent / '.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECRET_KEY: Leer de variable de entorno. Es VITAL que en prod sea un valor fuerte y único.
# En local, .env puede proveer DJANGO_SECRET_KEY.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'unvalorinseguro_por_defecto_cambiar_en_env_o_prod')

# DEBUG: Controlado por variable de entorno. Por defecto es False para seguridad.
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [] # Será poblado por local.py o prod.py

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Para servir estáticos con WhiteNoise en DEBUG=True
    'django.contrib.staticfiles',    # Debe ir después de whitenoise si usas runserver_nostatic
    # Mis apps
    'applications.administracion',
    'applications.almacen',
    'applications.home',
    'applications.operativo',
    'applications.proveedores',
    'applications.proyectos',
    'applications.usuariosdjango',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Justo después de SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

X_FRAME_OPTIONS = 'SAMEORIGIN' # Correcto para tus iframes

ROOT_URLCONF = 'ModeloMuestra.urls' # Esto estaba bien

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"], # Carpeta de templates a nivel de proyecto
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug', # Necesario si DEBUG=True
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ModeloMuestra.wsgi.application' # Correcto

# Database
# Configuración por defecto (SQLite), será sobreescrita por DATABASE_URL si está definida.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASE_URL_ENV = os.environ.get('DATABASE_URL')
if DATABASE_URL_ENV:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL_ENV)
    # Opcional: Configurar SSL para PostgreSQL en producción si es necesario
    # if 'postgres' in DATABASES['default']['ENGINE'] and not DEBUG: # Solo para prod
    #     DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}


AUTH_USER_MODEL = 'usuariosdjango.CustomUser' # Correcto

AUTH_PASSWORD_VALIDATORS = [ # Estándar, está bien
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# URLs de Login/Logout (usar nombres de URL es más robusto si son globales)
LOGIN_URL = 'login' 
LOGIN_REDIRECT_URL = 'inicio' # Usar nombre de URL
LOGOUT_REDIRECT_URL = 'login'

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles_build" # Carpeta donde collectstatic pondrá los archivos

# Configuración de WhiteNoise para servir estáticos (el storage se define en prod.py)
# STATICFILES_STORAGE se definirá en prod.py para producción.
# Para desarrollo, el default o whitenoise.runserver_nostatic es suficiente.

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'