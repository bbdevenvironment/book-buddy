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
CSRF_COOKIE_SECURE = True

# ==============================================================================
# CLOUDINARY STORAGE
# ==============================================================================
# Force remove conflicting apps to ensure Cloudinary takes priority
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in ["collectfasta", "storages"]]
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
        # Using StaticCloudinaryStorage (non-hashed) to bypass local file checks
        "BACKEND": "cloudinary_storage.storage.StaticCloudinaryStorage",
    },
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Required for Render to find files before uploading to Cloudinary
BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ==============================================================================
# DATABASES & EMAIL
# ==============================================================================
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)
ADMIN_URL = env("DJANGO_ADMIN_URL")

INSTALLED_APPS += ["anymail"]
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"