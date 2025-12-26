# config/settings/production.py
import os
from pathlib import Path
from .base import * # noqa: F403
from .base import DATABASES, INSTALLED_APPS, env

# ==============================================================================
# GENERAL & SECURITY
# ==============================================================================
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[".onrender.com"])

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_NAME = "__Secure-sessionid"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_NAME = "__Secure-csrftoken"
SECURE_HSTS_SECONDS = 31536000 # Increased for better security
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)

# ==============================================================================
# PATH CONFIGURATION (Fixed for Windows & Cloudinary)
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Force forward slashes to prevent "admin%5Ccss" errors on Cloudinary
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static').replace('\\', '/')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'edurock').replace('\\', '/')

# Ensure templates are also found correctly if they are in edurock/templates
TEMPLATES[0]['DIRS'] = [os.path.join(BASE_DIR, 'edurock', 'templates')]

# ==============================================================================
# DATABASES & CACHES
# ==============================================================================
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

REDIS_URL = env("REDIS_URL", default=None)
if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "IGNORE_EXCEPTIONS": True,
            },
        },
    }

# ==============================================================================
# CLOUDINARY STORAGE
# ==============================================================================
INSTALLED_APPS += ["cloudinary_storage", "cloudinary"]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env("CLOUDINARY_CLOUD_NAME"),
    'API_KEY': env("CLOUDINARY_API_KEY"),
    'API_SECRET': env("CLOUDINARY_API_SECRET"),
}

# config/settings/production.py

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "cloudinary_storage.storage.StaticCloudinaryStorage",
        # Adding this can help skip some upload issues
        "OPTIONS": {
            "IGNORE_EXCEPTIONS": True,
        }
    },
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# ==============================================================================
# EMAIL & ADMIN
# ==============================================================================
ADMIN_URL = env("DJANGO_ADMIN_URL")
INSTALLED_APPS += ["anymail"]
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
ANYMAIL = {}