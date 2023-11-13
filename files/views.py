import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import uuid

from .models import File, UserProfile
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from .serializers import FileSerializer
from django.http import JsonResponse, HttpResponseBadRequest


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.userprofile)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_files(request):
    is_admin = request.user.is_staff

    if is_admin and 'user_id' in request.query_params:
        target_user_id = request.query_params.get('user_id')
        try:
            target_user = UserProfile.objects.get(pk=target_user_id)
            user_files = File.objects.filter(user_profile=target_user)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        user_files = File.objects.filter(user_profile=request.user.userprofile)
    serializer = FileSerializer(user_files, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    if request.method == 'POST':
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User profile not found for the current user'}, status=400)

        try:
            data = request.data
            name = data.get('name')
            size = int(data.get('size'))
            mime_type = data.get('mime_type')
            file = File.objects.create(
                user_profile=user_profile,
                name=name,
                size=size,
                mime_type=mime_type,
                storage_path=data.get('path'),
            )

            return JsonResponse({'message': 'File uploaded successfully', 'file_id': file.id})
        except Exception as e:
            print(f"Error in upload_file: {e}")
            return JsonResponse({'error': 'An error occurred while processing the request'}, status=500)
    else:
        return HttpResponseBadRequest('Invalid request method')



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_file(request, file_id):
    try:
        file = File.objects.get(pk=file_id)
        if request.user != file.user_profile.user:
            raise PermissionDenied
        with open(file.path, 'rb') as file_content:
            response = HttpResponse(file_content.read(), content_type=file.mime_type)
        response['Content-Disposition'] = f'attachment; filename="{file.name}"'
        return response
    except File.DoesNotExist:
        return JsonResponse({'error': 'File not found'})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def rename_file(request, file_id):
    try:
        file = File.objects.get(pk=file_id)
        data = json.loads(request.body)
        new_name = data.get('new_name')
        file.name = new_name
        file.save()

        return JsonResponse({'message': 'File renamed successfully'})
    except File.DoesNotExist:
        return JsonResponse({'error': 'File not found'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_file(request, file_id):
    try:
        file = File.objects.get(pk=file_id)
        file.delete()
        return JsonResponse({'message': 'File deleted successfully'})
    except File.DoesNotExist:
        return JsonResponse({'error': 'File not found'})
