from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Определи UserProfileInline в административном интерфейсе
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

# Расширь UserAdmin, добавив UserProfileInline
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Перерегистрируй UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Зарегистрируй модель UserProfile
admin.site.register(UserProfile)
