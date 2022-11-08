from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views.views_user import UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView

urlpatterns = [
	path('', UserListView.as_view(), name='all_user'),
	path('<int:pk>/', UserDetailView.as_view(), name = 'one_user'),
	path('create/', UserCreateView.as_view(), name='create_user'),
	path('<int:pk>/update/', UserUpdateView.as_view(), name='update_user'),
	path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete_user'),
	path('login/', TokenObtainPairView.as_view()),
	path('login/refresh/', TokenRefreshView.as_view()),
]