from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.shortcuts import redirect
from django.views.static import serve 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('shop.urls')),
    path('', lambda request: redirect('/products/', permanent=True)),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]