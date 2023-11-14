from django.contrib import admin
from .models import File

class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'mime_type', 'storage_path', 'user_profile', 'upload_date', 'last_download_date')
    search_fields = ('name', 'user_profile__user__username')
    list_filter = ('user_profile__user__username', 'upload_date', 'last_download_date')

admin.site.register(File, FileAdmin)

