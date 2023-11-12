import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
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


@login_required
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User profile not found for the current user'}, status=400)

        try:
            data = json.loads(request.body)
            name = data.get('name')
            path = data.get('path')
            size = data.get('size')
            mime_type = data.get('mime_type')

            file = File.objects.create(
                user_profile=user_profile,
                name=name,
                path=path,
                size=size,
                mime_type=mime_type
            )

            return JsonResponse({'message': 'File uploaded successfully', 'file_id': file.id})
        except Exception as e:
            print(f"Error in upload_file: {e}")
            return JsonResponse({'error': 'An error occurred while processing the request'}, status=500)
    else:
        return HttpResponseBadRequest('Invalid request method')


@login_required
def get_file_list(request):
    user_profile = UserProfile.objects.get(user=request.user)
    files = File.objects.filter(user_profile=user_profile)
    file_list = [{'name': file.name, 'path': file.path, 'size': file.size, 'mime_type': file.mime_type,
                  'created_at': file.created_at, 'updated_at': file.updated_at} for file in files]
    return JsonResponse({'files': file_list})


@login_required
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


@login_required
@csrf_exempt
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


@login_required
def delete_file(request, file_id):
    try:
        file = File.objects.get(pk=file_id)
        file.delete()
        return JsonResponse({'message': 'File deleted successfully'})
    except File.DoesNotExist:
        return JsonResponse({'error': 'File not found'})
