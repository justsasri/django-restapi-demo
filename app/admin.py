from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Course, Lesson

# Lazy load swappable user model
User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Replace default django.contrib.auth.admin.UserAdmin"""
    pass


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass
