from django.contrib import admin
from django.urls import include, path,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('sales/', include('sales.urls')),
    path('preferences/', include('preferences.urls')),
    # path('preferences/', include('preferences.urls',namespace='preferences')),
    path('auth/', include('authentication.urls')),
    path('cart/', include('cart.urls')),
    path('dashboard/', include('dashboard.urls')),
    re_path(r'^api/.*$', TemplateView.as_view(template_name="index.html"))
  
      
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
