# polls/admin.py
from django.contrib import admin
from .models import Poll, PollOption

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'created_by')
    search_fields = ('title', 'description')

@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ('poll', 'option_text', 'votes')
    list_filter = ('poll',)
    search_fields = ('option_text',)

