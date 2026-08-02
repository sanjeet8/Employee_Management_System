from django.db import transaction
from apps.accounts.models import User
from apps.accounts.constants import UserRole
from .models import Employee
from django.db.models import Q
from django.contrib.auth.models import Group

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
        role,
        department,
        joining_date,
        employment_type,
        salary,
        is_active,
        manager=None,
    ):
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role,
        )
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)

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
    def get_visible_employees(user, search="", department=""):
        queryset = (Employee.objects.select_related(
            "user", "department", "manager"
        ))

        print("Current User:", user.username)
        print("Groups:", list(user.groups.values_list("name", flat=True)))
        # Role-based authorization will come here later.
        # Superuser can see everyone
        if user.is_superuser:
            pass
        
        # HR can see everyone
        elif user.groups.filter(name="HR").exists():
            print("Hey Hr you are Passing")
            pass

        # Manager can only see their team
        elif user.groups.filter(name="MANAGER").exists():
            queryset = queryset.filter(
                Q(manager=user.employee_profile) |
                Q(user = user)
            )
        
        # Employee can only see themselves
        else:
            print("Hey Hr you are failing")
            queryset = queryset.filter(
                user=user
            )

        if department:
            queryset = queryset.filter(
                department__name=department
            )
            
        if search:
            queryset = queryset.filter(
                Q(user__username__icontains=search) |
                Q(user__employee_id__icontains=search)
            )

        return queryset