
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from adverts_db import settings
from selection.views import SelectionViewSet
from user.views.views_location import LocationViewSet

router=routers.SimpleRouter()
router.register('location', LocationViewSet)
router.register('selection', SelectionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('cat/', include('category.urls')),
    path('adv/', include("advert.urls")),
    path('user/', include("user.urls")),
    # path('selection/', include("selection.urls")),
]
urlpatterns+=router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
