from django import forms
from .models import Poll, PollOption

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('title', 'description')

class PollOptionForm(forms.ModelForm):
    class Meta:
        model = PollOption
        fields = ('option_text',)

