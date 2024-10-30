from django.contrib import admin

# Register your models here.
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'display_name', 'email', 'year', 'department')
    list_filter = ('year', 'department')
    search_fields = ('username', 'email', 'display_name', 'student_id')
