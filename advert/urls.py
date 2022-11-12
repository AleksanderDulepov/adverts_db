from django.urls import path

from advert import views
from advert.views import AdvertListView, AdvertDetailView, AdvertCreateView, AdvertUpdateView, AdvertUpdateImageView, \
	AdvertDeleteView

urlpatterns = [
	path('', AdvertListView.as_view(), name='all_adv'),
	path('<int:pk>/', AdvertDetailView.as_view(), name='one_adv'),
	path('create/', AdvertCreateView.as_view(), name='create_adv'),
	path('<int:pk>/update/', AdvertUpdateView.as_view(), name='update_adv'),
	path('<int:pk>/upload_image/', AdvertUpdateImageView.as_view(), name='upload_image_adv'),
	path('<int:pk>/delete/', AdvertDeleteView.as_view(), name='delete_adv'),
]