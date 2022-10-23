from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from adverts_db import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cat/', include('category.urls')),
    path('adv/', include("advert.urls")),
    path('user/', include("user.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
