from django.db import models

class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    HR = "HR", "HR"
    MANAGER = "MANAGER", "Manager"
    EMPLOYEE = "EMPLOYEE", "Employee"