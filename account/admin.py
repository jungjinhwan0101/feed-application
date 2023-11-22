from django.contrib import admin
from django.contrib.admin import ModelAdmin

from account.models import User


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login', 'password',)
