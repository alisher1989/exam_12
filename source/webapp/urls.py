from django.urls import path

from webapp.views import IndexView, FileDetailView, FileCreateView, FileUpdateView, FileDeleteView, \
    AddUserToPrivateView, DeleteFromPrivateView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('file/<int:pk>/', FileDetailView.as_view(), name='file_detail_view'),
    path('file/create/', FileCreateView.as_view(), name='add_file'),
    path('file/<int:pk>/update/', FileUpdateView.as_view(), name='update_file'),
    path('file/<int:pk>/delete/', FileDeleteView.as_view(), name='delete_file'),
    path('add-to-private/', AddUserToPrivateView.as_view(), name='add-to-private'),
    path('delete-from-private/', DeleteFromPrivateView.as_view(), name='delete-from-favorites')
]

app_name = 'webapp'