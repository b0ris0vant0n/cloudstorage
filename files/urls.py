from django.urls import path
from .views import *

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('download/<int:file_id>', download_file, name='download_file'),
    path('get-files/', get_user_files, name='get_user_files'),
    path('rename/<int:file_id>', rename_file, name='rename_file'),
    path('delete/<int:file_id>', delete_file, name='delete_file'),
    path('comment/<int:file_id>', update_file_comment, name="update_comment"),
    path('share/<int:file_id>', share_file, name="share file"),
]

