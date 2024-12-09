from django import forms
from .models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('category', 'title', 'description')  # カテゴリを追加
        labels = {
            'title': 'タイトル',
            'description': '質問内容',
            'category': 'カテゴリ',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('content',)

