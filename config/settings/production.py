"""
Production Settings for Django on Render.com
"""

import os
from pathlib import Path
from .base import *  # noqa: F403

# ==============================================================================
# GENERAL
# ==============================================================================
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'dummy-secret-key-for-now')
ALLOWED_HOSTS = ['*']  # Allow all for debugging

# ==============================================================================
# PATHS - CRITICAL FIX
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ==============================================================================
# STATIC FILES - SIMPLIFIED APPROACH
# ==============================================================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Use Path objects converted to strings
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'edurock', 'static'),
]

# Use simple storage for now
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# ==============================================================================
# MEDIA FILES
# ==============================================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ==============================================================================
# TEMPLATES
# ==============================================================================
TEMPLATES[0]['DIRS'] = [os.path.join(BASE_DIR, 'edurock', 'templates')]

# ==============================================================================
# DATABASES
# ==============================================================================
DATABASES["default"]["CONN_MAX_AGE"] = 60

# ==============================================================================
# MIDDLEWARE - Add WhiteNoise
# ==============================================================================
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# ==============================================================================
# SECURITY - Disable temporarily for debugging
# ==============================================================================
# Comment these out temporarily
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# ==============================================================================
# DEBUG OUTPUT
# ==============================================================================
print("=" * 80)
print("PRODUCTION SETTINGS LOADED")
print(f"BASE_DIR: {BASE_DIR}")
print(f"STATIC_ROOT: {STATIC_ROOT}")
print(f"STATICFILES_DIRS: {STATICFILES_DIRS}")
print(f"DEBUG: {DEBUG}")
print("=" * 80)