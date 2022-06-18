from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Lazy load swappable user model
User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Replace default django.contrib.auth.admin.UserAdmin"""

    pass
