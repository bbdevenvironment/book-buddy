from django.urls import path
from pages.views import (root_page_view, dynamic_pages_view)
from edurock.views.debug import debug_static_files
app_name = 'pages'

urlpatterns = [
    path('', root_page_view, name="index"),
    path('<str:template_name>/', dynamic_pages_view, name='dynamic_pages'),
      path('debug-static/', debug_static_files, name='debug_static')
]
