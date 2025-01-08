from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=20, unique=True,blank=True)
    display_name = models.CharField(max_length=100, unique=False)
    year = models.PositiveIntegerField(blank=True, null=True)
    department = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True, validators=[MinValueValidator(0.0), MaxValueValidator(4.0) ] )
    circle = models.CharField(max_length=100, blank=True, null=True)
    
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # `auth.User.groups` との競合を避けるために追加
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # `auth.User.user_permissions` との競合を避けるために追加
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
    YEAR_CHOICES = [
        (1, '学部1年'),
        (2, '学部2年'),
        (3, '学部3年'),
        (4, '学部4年'),
        (5, '院生'),
        (6, '卒業生'),
        (7, '教職員'),
    ]
    
    # 他のフィールド...
    year = models.IntegerField(choices=YEAR_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.display_name  # 必要に応じて表示名を設定
    
    def save(self, *args, **kwargs):
        # メールアドレスの@前部分をstudent_idとして設定
        if not self.student_id and self.email:
            self.student_id = self.email.split('@')[0]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_name

class SignupToken(models.Model):
    email = models.EmailField(unique=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email