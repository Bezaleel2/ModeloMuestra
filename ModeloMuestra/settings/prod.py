# ModeloMuestra/settings/prod.py
import os
from .base import * # MUY IMPORTANTE: Importa todas las configuraciones base primero

# --- CONFIGURACIONES ESPECÍFICAS DE PRODUCCIÓN ---

# DEBUG: Siempre False en producción
DEBUG = False

# SECRET_KEY: DEBE ser cargada desde una variable de entorno en el servidor de Render.
# Asegúrate de que la variable de entorno en Render se llame DJANGO_SECRET_KEY (o la que uses en base.py)
# Si base.py usa os.environ.get('DJANGO_SECRET_KEY', ...), esta línea no es estrictamente necesaria
# aquí a menos que quieras asegurar que falle si no está definida, usando os.environ['DJANGO_SECRET_KEY']
# Por seguridad, es bueno que el programa falle si la clave de producción no está.
try:
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
except KeyError:
    raise Exception("ERROR: DJANGO_SECRET_KEY de producción no está configurada en el entorno!")


# ALLOWED_HOSTS: Configura con el dominio de tu aplicación en Render.
# Render provee RENDER_EXTERNAL_HOSTNAME automáticamente.
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME]
else:
    # Si por alguna razón RENDER_EXTERNAL_HOSTNAME no está disponible,
    # deberías tener un fallback o un error.
    # Como mínimo, para que el health check de Render funcione,
    # podrías necesitar añadir el nombre de tu servicio si lo conoces.
    # Ejemplo: ALLOWED_HOSTS = ['modelomuestra-web.onrender.com']
    # Es mejor confiar en RENDER_EXTERNAL_HOSTNAME si es posible.
    print("ADVERTENCIA: RENDER_EXTERNAL_HOSTNAME no encontrado. ALLOWED_HOSTS podría no estar configurado correctamente.")
    # ALLOWED_HOSTS = [] # O una lista vacía para forzar error si no se configura bien

# DATABASE:
# La configuración en base.py que lee DATABASE_URL del entorno ya debería funcionar.
# Render inyectará la variable de entorno DATABASE_URL.
# Opcional: Configurar SSL para PostgreSQL en producción si tu proveedor lo requiere
# y si dj_database_url no lo maneja automáticamente con la URL.
# if DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
#     DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}


# STATICFILES_STORAGE: Para WhiteNoise en producción con compresión y versionado.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- CONFIGURACIONES DE SEGURIDAD ADICIONALES PARA PRODUCCIÓN (RECOMENDADO) ---
CSRF_COOKIE_SECURE = True       # Solo enviar cookie CSRF sobre HTTPS
SESSION_COOKIE_SECURE = True    # Solo enviar cookie de sesión sobre HTTPS
SECURE_SSL_REDIRECT = True      # Redirigir todas las conexiones HTTP a HTTPS (si tu proxy/Render no lo hace ya)
SECURE_HSTS_SECONDS = 2592000   # 30 días. Aumentar después de confirmar que todo funciona.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# X_FRAME_OPTIONS = 'SAMEORIGIN' # Ya está en base.py, se hereda.

# Configuración de Email para producción (debes configurar un servicio de email real)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get('EMAIL_HOST')
# EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
# EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'webmaster@tu_dominio.com')
# SERVER_EMAIL = DEFAULT_FROM_EMAIL # Para correos de error del servidor

# Logging - Configura un logging más robusto para producción
# ... (ejemplo básico, puedes expandirlo mucho más)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING', # Solo WARNING y superior en producción
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'), # INFO para Django en prod
            'propagate': False,
        },
    },
}