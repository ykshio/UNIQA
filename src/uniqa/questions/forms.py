from django import forms
from .models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('category', 'title', 'description', 'image')  # カテゴリを追加
        labels = {
            'title': 'タイトル',
            'description': '質問内容',
            'category': 'カテゴリ',
            'image': '画像',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('content','image')
        labels = {
            'content':'回答内容',
            'image': '画像',
        }

