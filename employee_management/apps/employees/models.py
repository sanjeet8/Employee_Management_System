from django.db import models
from django.conf import settings

from apps.departments.models import Department

# Create your models here.
class EmploymentType(models.TextChoices):
    FULL_TIME = "FULL_TIME", "Full Time"
    PART_TIME = "PART_TIME", "Part Time"
    INTERN = "INTERN", "Intern"
    CONTRACT = "CONTRACT", "Contract"

class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_profile",
    )

    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name="employees",
    )

    manager = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True,
    )

    joining_date = models.DateField()

    employment_type = models.CharField(
        max_length=20, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME,
    )

    salary = models.DecimalField(max_digits=10, decimal_places=2,)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "employees"
        ordering = ["user__employee_id"]

    def __str__(self):
        return f"{self.user.employee_id} - {self.user.get_full_name()}"