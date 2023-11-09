from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile


class File(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    size = models.IntegerField()
    mime_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    is_private = models.BooleanField(default=False)