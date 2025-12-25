# production.py
from .base import *
from .base import DATABASES, INSTALLED_APPS, env, TEMPLATES

# 1. STOP THE CRASHING (Critical for WhiteNoise)
# ------------------------------------------------------------------------------
# This prevents the ValueError: Missing staticfiles manifest entry crash
WHITENOISE_MANIFEST_STRICT = False 

# 2. GENERAL & SECURITY
# ------------------------------------------------------------------------------
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["book-buddy-4i7i.onrender.com", ".onrender.com"])
DEBUG = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ["https://book-buddy-4i7i.onrender.com", "https://*.onrender.com"]

# 3. CLOUDINARY (Using your "book buddy" preset)
# ------------------------------------------------------------------------------
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in ["cloudinary_storage", "cloudinary"]]
INSTALLED_APPS = ["cloudinary_storage"] + INSTALLED_APPS + ["cloudinary"]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env("CLOUDINARY_CLOUD_NAME"),
    'API_KEY': env("CLOUDINARY_API_KEY"),
    'API_SECRET': env("CLOUDINARY_API_SECRET"),
    'SECURE': True,
    'UPLOAD_PRESET': 'book buddy', 
}

# 4. STORAGES
# ------------------------------------------------------------------------------
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# 5. TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG