"""
Production Settings for Django on Render.com
"""

import os
from pathlib import Path
from .base import *  # noqa: F403
from .base import DATABASES, INSTALLED_APPS, MIDDLEWARE, env, TEMPLATES

# ==============================================================================
# GENERAL & SECURITY
# ==============================================================================
DEBUG = False
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[".onrender.com", "localhost"])

# Security settings for production
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
SECURE_BROWSER_XSS_FILTER = env.bool("DJANGO_SECURE_BROWSER_XSS_FILTER", default=True)

# ==============================================================================
# PATHS
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ==============================================================================
# STATIC FILES CONFIGURATION
# ==============================================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Static files directories
STATICFILES_DIRS = [
    BASE_DIR / 'edurock' / 'static',
]

# Use ManifestStaticFilesStorage for better cache control
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# ==============================================================================
# MEDIA FILES
# ==============================================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==============================================================================
# TEMPLATES
# ==============================================================================
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'edurock' / 'templates']

# Update template settings for production
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# ==============================================================================
# DATABASES
# ==============================================================================
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

# ==============================================================================
# CACHING
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
                "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            },
        },
    }
else:
    # Fallback to local memory cache
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    }

# ==============================================================================
# LOGGING
# ==============================================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# ==============================================================================
# EMAIL CONFIGURATION
# ==============================================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='webmaster@localhost')

# ==============================================================================
# PERFORMANCE OPTIMIZATIONS
# ==============================================================================
# Database connection persistency
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

# Session engine with cache
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

# ==============================================================================
# APPLICATION SPECIFIC SETTINGS
# ==============================================================================
ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")

# ==============================================================================
# SECURITY HEADERS
# ==============================================================================
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
X_FRAME_OPTIONS = 'DENY'

# ==============================================================================
# CLOUDINARY CONFIGURATION (Optional)
# ==============================================================================
CLOUDINARY_CLOUD_NAME = env("CLOUDINARY_CLOUD_NAME", default=None)
CLOUDINARY_API_KEY = env("CLOUDINARY_API_KEY", default=None)
CLOUDINARY_API_SECRET = env("CLOUDINARY_API_SECRET", default=None)

if all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
    INSTALLED_APPS += ["cloudinary_storage", "cloudinary"]
    
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
        'API_KEY': CLOUDINARY_API_KEY,
        'API_SECRET': CLOUDINARY_API_SECRET,
        'SECURE': True,
    }
    
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # Use local file storage if Cloudinary not configured
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# ==============================================================================
# WHITENOISE CONFIGURATION FOR BETTER STATIC FILES SERVING
# ==============================================================================
# Add WhiteNoise middleware
MIDDLEWARE.insert(
    1,  # Right after SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
)

# WhiteNoise configuration for better performance
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_ALLOW_ALL_ORIGINS = True

# ==============================================================================
# FINAL SETUP
# ==============================================================================
# Ensure DEBUG is False in production (override any other settings)
DEBUG = False

# Remove duplicate 'staticfiles' from INSTALLED_APPS if exists
# This is the fix for the error
if 'django.contrib.staticfiles' in INSTALLED_APPS:
    # Already included, don't add again
    pass
else:
    INSTALLED_APPS += ['django.contrib.staticfiles']

# Log current settings for debugging
print(f"DEBUG: Static URL: {STATIC_URL}")
print(f"DEBUG: Static Root: {STATIC_ROOT}")
print(f"DEBUG: Static Dirs: {[str(d) for d in STATICFILES_DIRS]}")
print(f"DEBUG: Debug Mode: {DEBUG}")
print(f"DEBUG: Allowed Hosts: {ALLOWED_HOSTS}")
print(f"DEBUG: Staticfiles in INSTALLED_APPS: {'django.contrib.staticfiles' in INSTALLED_APPS}")