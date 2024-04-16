
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path("admin/", admin.site.urls),
    path("api/", include('secqr_api.api.urls')),
    path("api/", include('account.urls'))
] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
