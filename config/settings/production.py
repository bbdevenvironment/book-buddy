# production.py
# ruff: noqa: E501
from .base import * # noqa: F403
from .base import DATABASES, INSTALLED_APPS, env, TEMPLATES

# GENERAL
# ------------------------------------------------------------------------------
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["book-buddy-4i7i.onrender.com", ".onrender.com"])
DEBUG = False

# DATABASES
# ------------------------------------------------------------------------------
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

# CACHES
# ------------------------------------------------------------------------------
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

# SECURITY
# ------------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    "https://book-buddy-4i7i.onrender.com",
    "https://*.onrender.com"
] + env.list("CSRF_TRUSTED_ORIGINS", default=[])
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# CLOUDINARY STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in ["cloudinary_storage", "cloudinary"]]
INSTALLED_APPS = ["cloudinary_storage"] + INSTALLED_APPS + ["cloudinary"]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env("CLOUDINARY_CLOUD_NAME"),
    'API_KEY': env("CLOUDINARY_API_KEY"),
    'API_SECRET': env("CLOUDINARY_API_SECRET"),
    'SECURE': True,
}

# STORAGES (Fixes "Mutually Exclusive" and "InvalidStorage" errors)
# ------------------------------------------------------------------------------
# Clear legacy keys imported from base.py
if "STATICFILES_STORAGE" in globals():
    del STATICFILES_STORAGE
if "DEFAULT_FILE_STORAGE" in globals():
    del DEFAULT_FILE_STORAGE

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL", default="Book Buddy <noreply@book-buddy-4i7i.onrender.com>")
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG