from rest_framework import serializers
from .models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'user_profile', 'name', 'path', 'size', 'mime_type', 'created_at', 'updated_at']
