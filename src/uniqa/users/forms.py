from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from PIL import Image

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'student_id', 'display_name', 'year', 'department', 'icon', 'gpa', 'circle')

class CustomUserChangeForm(UserChangeForm):
    YEAR_CHOICES = [
        (1, '学部1年'),
        (2, '学部2年'),
        (3, '学部3年'),
        (4, '学部4年'),
        (5, '院生'),
        (6, '卒業生'),
        (7, '教職員'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('AD', 'システムデザイン工学部デザイン工学科'),
        ('AJ', 'システムデザイン工学部情報システム工学科'),
        ('EC', '工学部情報通信工学科'),
        ('EF', '工学部先端機械工学科'),
        ('EH', '工学部電子システム工学科'),
        ('EJ', '工学部電気電子工学科'),
        ('EK', '工学部機械工学科'),
        ('ES', '工学部応用化学科'),
        ('FA', '未来科学部建築学科'),
        ('FI', '未来科学部情報メディア学科'),
        ('FR', '未来科学部ロボット・メカトロニクス学科'),
    ]

    year = forms.ChoiceField(choices=YEAR_CHOICES, required=False, label='学年')
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, required=False, label='学科')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # year の表示を更新する
        if self.instance.pk:
            self.fields['year'].initial = self.instance.get_year_display()

    class Meta:
        model = CustomUser
        fields = ('display_name', 'year', 'department', 'icon', 'gpa', 'circle')
        labels = {
            'display_name': '表示名',
            'year': '学年',
            'department': '学科',
            'icon': 'アイコン(最大サイズ：128px × 128px)',
            'gpa': 'GPA',
            'circle': '所属サークル',
        }

    def clean_gpa(self):
        gpa = self.cleaned_data.get('gpa')
        if gpa is not None and (gpa < 0 or gpa > 4):
            raise ValidationError('GPAは0以上4以下である必要があります。')
        return gpa

    def clean_icon(self):
        icon = self.cleaned_data.get('icon')
        if icon:
            try:
                img = Image.open(icon)
                if img.size != (128, 128):
                    raise ValidationError('アイコン画像のサイズは128x128である必要があります。')
            except Exception:
                raise ValidationError('有効な画像ファイルをアップロードしてください。')
        return icon
