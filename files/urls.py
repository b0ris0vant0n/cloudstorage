from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('get-list/', views.get_file_list, name='get_file_list'),
    path('rename/<int:file_id>/', views.rename_file, name='rename_file'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
]
