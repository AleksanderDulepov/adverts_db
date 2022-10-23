from django.urls import path

from category.views import CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, \
	CategoryDeleteView

urlpatterns = [
	path('', CategoryListView.as_view(), name='all_cat'),
	path('<int:pk>/', CategoryDetailView.as_view(), name='one_cat'),
	path('create/', CategoryCreateView.as_view(), name='create_cat'),
	path('<int:pk>/update/', CategoryUpdateView.as_view(), name='update_cat'),
	path('<int:pk>/delete/', CategoryDeleteView.as_view(), name='delete_cat'),
]