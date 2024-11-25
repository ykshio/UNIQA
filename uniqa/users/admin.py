from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'display_name', 'email', 'student_id', 'year', 'department', 'gpa', 'circle', 'is_staff', 'is_active')
    search_fields = ('email', 'student_id', 'display_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)