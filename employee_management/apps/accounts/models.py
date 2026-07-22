from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from .constants import UserRole

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    employee_id = models.CharField(max_length=20, unique=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.EMPLOYEE,
    )

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"