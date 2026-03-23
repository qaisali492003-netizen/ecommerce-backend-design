from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect # 1. Import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('shop.urls')),
    
    # 2. Redirect the root URL ('') to your products page
    path('', lambda request: redirect('products/', permanent=True)),
]

# This adds the media path to the existing list
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)