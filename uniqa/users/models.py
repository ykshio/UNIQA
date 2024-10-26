from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    student_id = models.CharField(max_length=20, unique=True)
    year = models.PositiveIntegerField()
    department = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)


