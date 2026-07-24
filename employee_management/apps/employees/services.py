from django.db import transaction
from apps.accounts.models import User
from apps.accounts.constants import UserRole
from apps.departments.models import Department
from .models import Employee

class EmployeeService:

    @staticmethod
    @transaction.atomic
    def create_employee(
        *,
        username,
        password,
        first_name,
        last_name,
        email,
        department,
        joining_date,
        employment_type,
        salary,
        manager=None,
        role=UserRole.EMPLOYEE,
    ):
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role,
        )

        employee = Employee.objects.create(
            user=user,
            department=department,
            joining_date=joining_date,
            employment_type=employment_type,
            salary=salary,
            manager=manager,
        )

        return employee