from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from rest_framework import viewsets, permissions
from .serializers import UserProfileSerializer, UserSerializer

from cloudstorageserver.logger import setup_logger

from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

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
        user_serializer = UserSerializer(data=request.data.get('user'))
        profile_serializer = UserProfileSerializer(data=request.data)
        if user_serializer.is_valid() and profile_serializer.is_valid():
            user = user_serializer.save()
            profile_serializer.save(user=user)
            return Response({'message': 'User registered successfully'})
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error in register_user: {e}")
        return Response({'error': 'An error occurred while processing the request'}, status=500)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user_list(request):
    try:
        users = UserProfile.objects.all()
        user_list = [
            {'username': user.user.username, 'full_name': user.full_name, 'email': user.email, 'is_admin': user.is_admin,
             'storage_path': user.storage_path} for user in users]
        return JsonResponse({'users': user_list})
    except Exception as e:
        logger.error(f"Error in register_user: {e}")
        return Response({'error': 'An error occurred while processing the request'}, status=500)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
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

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


@api_view(['GET'])
def user_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})
