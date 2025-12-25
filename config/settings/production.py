# ruff: noqa: E501
import os
from pathlib import Path
from .base import * # noqa: F403
from .base import DATABASES, INSTALLED_APPS, env

# ==============================================================================
# GENERAL & SECURITY
# ==============================================================================
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["book-buddy-4i7i.onrender.com", ".onrender.com"])

# Debug should always be False in production
DEBUG = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ==============================================================================
# CLOUDINARY STORAGE
# ==============================================================================
# Clean up INSTALLED_APPS before adding cloudinary
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in ["cloudinary_storage", "cloudinary", "storages"]]

# Add Cloudinary apps in correct order
INSTALLED_APPS = ["cloudinary_storage"] + INSTALLED_APPS + ["cloudinary"]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env("CLOUDINARY_CLOUD_NAME"),
    'API_KEY': env("CLOUDINARY_API_KEY"),
    'API_SECRET': env("CLOUDINARY_API_SECRET"),
    'SECURE': True,
    'STATIC_IMAGES_EXTENSIONS': ['jpg', 'jpeg', 'png', 'gif', 'svg', 'ico', 'webp'],
    'STATICFILES_MANIFEST_ROOT': os.path.join(BASE_DIR, 'static'),
}

# Cloudinary storage configuration
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "cloudinary_storage.storage.StaticHashedCloudinaryStorage",
        # Or use this for non-hashed files:
        # "BACKEND": "cloudinary_storage.storage.StaticCloudinaryStorage",
    },
}

# Static and media URLs
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Required for static file collection
BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Tell Django to look for static files in these directories
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# ==============================================================================
# WHITENOISE FOR STATIC FILES (Alternative to Cloudinary for static files)
# ==============================================================================
# If Cloudinary isn't working for static files, consider using Whitenoise instead:
# INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')
# MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
# STORAGES = {
#     "default": {
#         "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
#     },
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================================================================
# DATABASES & EMAIL
# ==============================================================================
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)
ADMIN_URL = env("DJANGO_ADMIN_URL")

INSTALLED_APPS += ["anymail"]
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# ==============================================================================
# TEMPLATE CONFIGURATION
# ==============================================================================
# Ensure templates are configured correctly for production
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG