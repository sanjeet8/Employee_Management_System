from django.db import transaction
from apps.accounts.models import User
from apps.accounts.constants import UserRole
from .models import Employee
from django.db.models import Q
from django.contrib.auth.models import Group

class EmployeeService:

    @staticmethod
    def _assign_group(user, role):
        user.groups.clear()
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)

    @staticmethod
    def _extract_user_data(validated_data):
        return {
            "first_name": validated_data.pop("first_name"),
            "last_name": validated_data.pop("last_name"),
            "email": validated_data.pop("email"),
            "role": validated_data.pop("role"),
        }


    @staticmethod
    @transaction.atomic
    def create_employee(*, validated_data):
        username = validated_data.pop("username")
        password = validated_data.pop("password")

        # Extract user data
        role = validated_data.pop("role")
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        email = validated_data.pop("email")

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role,
        )
        EmployeeService._assign_group(user, role)

        employee = Employee.objects.create(
            user=user,
            **validated_data
        )

        return employee
    
    @staticmethod
    @transaction.atomic
    def update_employee(*, employee: Employee, validated_data):
        user = employee.user

        # Extract user data
        role = validated_data.pop("role")
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        email = validated_data.pop("email")

        # Update User
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.role = role
        user.save()

        # Update Employee
        for field, value in validated_data.items():
            setattr(employee, field, value)
        employee.save()

        # Update the Group
        EmployeeService._assign_group(user, role)

    @staticmethod
    @transaction.atomic
    def deactivate_employee(*, employee: Employee):
        # Deactivate employee
        employee.is_active = False
        employee.save()

        # Disable login
        employee.user.is_active = False
        employee.user.save()

        # Remove as manager from team members
        Employee.objects.filter(
            manager = employee
        ).update(manager=None)

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