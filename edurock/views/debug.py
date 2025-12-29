from django.http import JsonResponse
from django.contrib.staticfiles import finders
import os

def debug_static_files(request):
    """Endpoint to debug static files issues"""
    results = {}
    
    # Test static file paths
    test_files = [
        'js/vendor/jquery-3.6.0.min.js',
        'js/bootstrap.min.js',
        'js/bootstrap.bundle.min.js',
        'js/popper.min.js',
        'js/vendor/modernizr-3.5.0.min.js',
        'css/bootstrap.min.css',
        'css/style.css',
        'img/favicon.png',
    ]
    
    for file_path in test_files:
        found_path = finders.find(file_path)
        results[file_path] = {
            'requested': file_path,
            'found': bool(found_path),
            'absolute_path': found_path,
            'exists': os.path.exists(found_path) if found_path else False,
            'static_url': f"/static/{file_path}"
        }
    
    return JsonResponse({
        'static_settings': {
            'STATIC_URL': request.build_absolute_uri('/static/'),
            'STATIC_ROOT': str(STATIC_ROOT),
            'STATICFILES_DIRS': [str(d) for d in STATICFILES_DIRS],
        },
        'files': results,
        'environment': {
            'DEBUG': DEBUG,
            'ALLOWED_HOSTS': ALLOWED_HOSTS,
        }
    })