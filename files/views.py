import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import File, UserProfile


@login_required
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)

        # Получаем данные из запроса
        data = json.loads(request.body)
        name = data.get('name')
        path = data.get('path')  # относительный путь к файлу
        size = data.get('size')
        mime_type = data.get('mime_type')

        # Создаем файл
        file = File.objects.create(user_profile=user_profile, name=name, path=path, size=size, mime_type=mime_type)

        return JsonResponse({'message': 'File uploaded successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


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
        # Реализуй логику для скачивания файла
        # Вероятно, тебе понадобится использовать HttpResponse и установить соответствующие заголовки.
        return JsonResponse({'message': 'File downloaded successfully'})
    except File.DoesNotExist:
        return JsonResponse({'error': 'File not found'})


@login_required
@csrf_exempt
def rename_file(request, file_id):
    try:
        file = File.objects.get(pk=file_id)
        # Получаем данные из запроса
        data = json.loads(request.body)
        new_name = data.get('new_name')

        # Переименовываем файл
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
