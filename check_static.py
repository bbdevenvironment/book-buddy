#!/usr/bin/env python
import os
import sys

# Add project to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

import django
django.setup()

from django.conf import settings
from django.contrib.staticfiles import finders
from pathlib import Path

print("=" * 80)
print("CHECKING STATIC FILES")
print("=" * 80)

# Check settings
print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"STATIC_URL: {settings.STATIC_URL}")
print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
print(f"BASE_DIR: {settings.BASE_DIR}")

# Check if source static files exist
source_static = Path(settings.BASE_DIR) / 'edurock' / 'static'
print(f"\nSource static directory exists: {source_static.exists()}")
print(f"Source static directory: {source_static}")

if source_static.exists():
    # List JS files
    js_files = list(source_static.rglob('*.js'))
    print(f"\nFound {len(js_files)} JS files in source:")
    for js in js_files[:20]:  # Show first 20
        print(f"  - {js.relative_to(source_static)}")
    
    # List vendor JS files
    vendor_js = list((source_static / 'js' / 'vendor').glob('*.js'))
    print(f"\nFound {len(vendor_js)} vendor JS files:")
    for js in vendor_js:
        print(f"  - {js.name}")

# Check if staticfiles directory exists
staticfiles_dir = Path(settings.STATIC_ROOT)
print(f"\nStaticfiles directory exists: {staticfiles_dir.exists()}")

if staticfiles_dir.exists():
    # List collected JS files
    collected_js = list(staticfiles_dir.rglob('*.js'))
    print(f"Found {len(collected_js)} JS files in staticfiles:")
    for js in collected_js[:20]:
        print(f"  - {js.relative_to(staticfiles_dir)}")

print("\n" + "=" * 80)