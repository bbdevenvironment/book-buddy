import os
from pathlib import Path
from .base import * # noqa: F403
from .base import DATABASES, INSTALLED_APPS, MIDDLEWARE, env, TEMPLATES

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
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)

# ==============================================================================
# MIDDLEWARE (WhiteNoise Setup)
# ==============================================================================
MIDDLEWARE.insert(
    MIDDLEWARE.index("django.middleware.security.SecurityMiddleware") + 1,
    "whitenoise.middleware.WhiteNoiseMiddleware",
)

# SAFETY SETTINGS
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_USE_FINDERS = True

# ==============================================================================
# PATH CONFIGURATION
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Standardized path joining for Render's Linux environment
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'edurock', 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
TEMPLATES[0]['DIRS'] = [os.path.join(BASE_DIR, 'edurock', 'templates')]

# ==============================================================================
# STORAGE CONFIGURATION
# ==============================================================================
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
        # Using the standard StaticFilesStorage is safer when path issues persist
        "BACKEND": "whitenoise.storage.StaticFilesStorage",
    },
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

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

ADMIN_URL = env("DJANGO_ADMIN_URL")
INSTALLED_APPS += ["anymail"]
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
ANYMAIL = {}