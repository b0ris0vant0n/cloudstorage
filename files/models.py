from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile


class File(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    size = models.PositiveIntegerField()
    mime_type = models.CharField(max_length=255, default='text')
    upload_date = models.DateTimeField(auto_now_add=True)
    last_download_date = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True)
    storage_path = models.CharField(max_length=255)
    special_link = models.CharField(max_length=255, unique=True, blank=True, null=True)