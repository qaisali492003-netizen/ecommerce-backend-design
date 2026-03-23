from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.views.static import serve # Add this import
import re # Add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('shop.urls')),
    path('', lambda request: redirect('products/', permanent=True)),
    
    # This force-serves media files even when DEBUG is False
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]