# questions/admin.py
from django.contrib import admin
from .models import Question, Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'created_by')
    search_fields = ('title', 'description')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'content', 'created_at', 'created_by')
    list_filter = ('question',)
    search_fields = ('content',)

