# questions/admin.py
from django.contrib import admin
from .models import Question, Answer, Category

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'is_resolved')
    search_fields = ('title', 'description', 'created_by__display_name')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'content', 'created_at', 'created_by')
    list_filter = ('question',)
    search_fields = ('content', 'created_by__display_name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)