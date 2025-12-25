# ruff: noqa: E501
import os
from pathlib import Path
from .base import * # noqa: F403
from .base import DATABASES, INSTALLED_APPS, env

# ==============================================================================
# GENERAL
# ==============================================================================
SECRET_KEY = env("DJANGO_SECRET_KEY")

# Allow Render subdomains
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[".onrender.com"])

# ==============================================================================
# DATABASES
# ==============================================================================
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

# ==============================================================================
# CACHES
# ==============================================================================
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
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        },
    }

# ==============================================================================
# SECURITY
# ==============================================================================
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
# CLOUDINARY STORAGE
# ==============================================================================
# 1. Add Cloudinary to Installed Apps
INSTALLED_APPS += ["cloudinary_storage", "cloudinary"]

# 2. Configure Cloudinary Credentials
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env("CLOUDINARY_CLOUD_NAME"),
    'API_KEY': env("CLOUDINARY_API_KEY"),
    'API_SECRET': env("CLOUDINARY_API_SECRET"),
}

# 3. Set Backends
# We use StaticCloudinaryStorage (not Hashed) to prevent the NoneType error
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "cloudinary_storage.storage.StaticCloudinaryStorage",
    },
}

# 4. Define URLs
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# 5. Local Path Configuration (Crucial for collectstatic to work on Render)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ==============================================================================
# EMAIL / ADMIN
# ==============================================================================
DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL", default="edurock <noreply@example.com>")
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX", default="[edurock] ")
ADMIN_URL = env("DJANGO_ADMIN_URL")

# ==============================================================================
# ANYMAIL
# ==============================================================================
INSTALLED_APPS += ["anymail"]
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
ANYMAIL = {}

# ==============================================================================
# COLLECTFASTA
# ==============================================================================
# Note: Cloudinary is highly optimized; Collectfasta is often redundant here.
INSTALLED_APPS = ["collectfasta", *INSTALLED_APPS]

# ==============================================================================
# LOGGING
# ==============================================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", "mail_admins"],
            "propagate": True,
        },
    },
}