from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile
import json


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        # Получаем данные из запроса
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        full_name = data.get('full_name')
        email = data.get('email')
        is_admin = data.get('is_admin', False)
        storage_path = data.get('storage_path')

        # Создаем пользователя
        user = User.objects.create_user(username=username, password=password, email=email)
        user_profile = UserProfile.objects.create(user=user, full_name=full_name, is_admin=is_admin, storage_path=storage_path)

        return JsonResponse({'message': 'User registered successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


@login_required
def get_user_list(request):
    users = UserProfile.objects.all()
    user_list = [{'username': user.user.username, 'full_name': user.full_name, 'email': user.email, 'is_admin': user.is_admin, 'storage_path': user.storage_path} for user in users]
    return JsonResponse({'users': user_list})


@login_required
def delete_user(request, user_id):
    try:
        user_profile = UserProfile.objects.get(pk=user_id)
        user_profile.user.delete()
        return JsonResponse({'message': 'User deleted successfully'})
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'})


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        # Получаем данные из запроса
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        # Аутентификация пользователя
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


@login_required
def user_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})
