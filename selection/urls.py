# from django.urls import path
#
# from selection.views import SelectionListView, SelectionDetailView, SelectionCreateView, SelectionUpdateView, \
#     SelectionDeleteView
#
# urlpatterns = [
# 	path('', SelectionListView.as_view(), name='all_selection'),
# 	path('<int:pk>/', SelectionDetailView.as_view(), name = 'one_selection'),
# 	path('create/', SelectionCreateView.as_view(), name='create_selection'),
# 	path('<int:pk>/update/', SelectionUpdateView.as_view(), name='update_selection'),
# 	path('<int:pk>/delete/', SelectionDeleteView.as_view(), name='delete_selection'),
#
# ]