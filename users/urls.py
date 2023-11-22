from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import UserProfileViewSet, register_user, get_user_list, delete_user, user_login, user_logout

router = DefaultRouter()
router.register(r'userprofiles', UserProfileViewSet)

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('get-users', get_user_list, name='get_user_list'),
    path('delete/<int:user_id>', delete_user, name='delete_user'),
    path('login/', user_login, name='user_login'),
    path('logout', user_logout, name='user_logout'),
    path('', include(router.urls)),
]