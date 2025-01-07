from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image

def validate_icon(image):
    img = Image.open(image)
    if img.height > 128 or img.width > 128:
        raise ValidationError("Icon size should be 128x128 pixels or smaller.")
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=20, unique=True,blank=True)
    display_name = models.CharField(max_length=100, unique=False)
    year = models.PositiveIntegerField(blank=True, null=True)
    department = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='icons/', null=True, blank=True, validators=[validate_icon])
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