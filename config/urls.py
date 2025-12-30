# ruff: noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    
    # User management
    path("users/", include("edurock.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    
    # Your stuff: custom urls includes go here
    path("", include("edurock.pages.urls", namespace="pages")),
    
    # Media files (Current version you had)
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

# Serving static files during development
if settings.DEBUG:
    # 1. This allows the error pages to be debugged during development
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]

    # 2. SERVE STATIC FILES (Crucial Fix)
    # This maps /static/ to your edurock/static/ folder
    if settings.STATIC_URL:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

    # 3. Enable Debug Toolbar
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns