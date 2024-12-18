from django.contrib import admin

# Register your models here.
from .models import Like

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username', 'question__title', 'answer__text')
