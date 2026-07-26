from django.db import transaction
from apps.accounts.models import User
from apps.accounts.constants import UserRole
from .models import Employee
from django.db.models import Q

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
    
    
    @staticmethod
    def get_visible_employees(user, search=""):
        queryset = (Employee.objects.select_related(
            "user", "department", "manager"
        ))

        # Role-based authorization will come here later.
        if search:
            queryset = queryset.filter(
                Q(user__username__icontains=search) |
                Q(user__employee_id__icontains=search)
            )

        return queryset