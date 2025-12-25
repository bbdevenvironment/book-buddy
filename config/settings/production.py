# ruff: noqa: E501
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
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)

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
# CLOUDINARY STORAGE (Corrected)
# ==============================================================================
# Removed 'storages' (AWS) and 'collectfasta' to prevent conflicts
INSTALLED_APPS += ["cloudinary_storage", "cloudinary"]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env("CLOUDINARY_CLOUD_NAME"),
    'API_KEY': env("CLOUDINARY_API_KEY"),
    'API_SECRET': env("CLOUDINARY_API_SECRET"),
}

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        # Using StaticCloudinaryStorage instead of Hashed to avoid path errors
        "BACKEND": "cloudinary_storage.storage.StaticCloudinaryStorage",
    },
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Ensure local path exists for Render to collect files before upload
BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ==============================================================================
# EMAIL & ADMIN
# ==============================================================================
ADMIN_URL = env("DJANGO_ADMIN_URL")
INSTALLED_APPS += ["anymail"]
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
ANYMAIL = {}