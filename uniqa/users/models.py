from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    student_id = models.CharField(max_length=20, unique=True)
    display_name = models.CharField(max_length=100, unique=False)
    year = models.PositiveIntegerField()
    department = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
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

    def __str__(self):
        return self.display_name

