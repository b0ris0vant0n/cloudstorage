from django.http import JsonResponse, HttpResponse
import re
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework import viewsets, permissions
from .serializers import UserProfileSerializer, UserSerializer
import base64

from cloudstorageserver.logger import setup_logger


logger = setup_logger(__name__)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    try:
        user_data = request.data.get('user')

        username = user_data.get('username')
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9]{3,19}$', username):
            return Response({'error': 'Такой логин не допустим'}, status=status.HTTP_400_BAD_REQUEST)

        email = user_data.get('email')
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return Response({'error': 'Неверно указан email'}, status=status.HTTP_400_BAD_REQUEST)

        password = user_data.get('password')
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$', password):
            return Response({'error': 'Неверно указан пароль'}, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(data=user_data)
        profile_serializer = UserProfileSerializer(data=request.data)

        if user_serializer.is_valid() and profile_serializer.is_valid():
            user = user_serializer.save()
            user.set_password(user_data['password'])
            user.save()
            profile_serializer.save(user=user)
            return Response({'message': 'User registered successfully'})
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error in register_user: {e}")
        return Response({'error': 'An error occurred while processing the request'}, status=500)


@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAdminUser])
def get_user_list(request):
    try:
        users = UserProfile.objects.all()
        user_list = [
            {'id': user.id, 'username': user.user.username, 'full_name': user.full_name, 'email': user.email, 'is_admin': user.is_admin,
             'storage_path': user.storage_path} for user in users]
        return JsonResponse({'users': user_list})
    except Exception as e:
        logger.error(f"Error in register_user: {e}")
        return Response({'error': 'An error occurred while processing the request'}, status=500)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
@csrf_exempt
def delete_user(request, user_id):
    try:
        user_profile = UserProfile.objects.get(pk=user_id)
        user_profile.user.delete()
        return JsonResponse({'message': 'User deleted successfully'})
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({'error': 'Both username and password are required'}, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token = RefreshToken.for_user(user)
            token_value = str(token)
            credentials = f"{username}:{password}"
            base64_credentials = base64.b64encode(credentials.encode()).decode("utf-8")

            return JsonResponse({
                'message': 'Login successful',
                'isAdmin': user.is_staff,
                'token': token_value,
                'authorization': f"Basic {base64_credentials}",
                'currentuser' : username,
            })
        else:
            logger.error(f'Failed login attempt for user: {username}')
            return JsonResponse({'error': 'Неверные логин или пароль'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method'})


@api_view(['GET'])
@csrf_exempt
def user_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})
