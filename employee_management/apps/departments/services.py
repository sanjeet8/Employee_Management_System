from django.db import transaction
from django.db.models import Q, Count

from apps.accounts.constants import UserRole
from apps.employees.models import Employee

from .models import Department

class DepartmentService:
    @staticmethod
    @transaction.atomic
    def create_department(*, validated_data):
        validated_data.pop("manager", None)

        return Department.objects.create(
            **validated_data
        )
    
    @staticmethod
    @transaction.atomic
    def assign_manager(*, department, manager):
        if manager.department_id != department.id:
            raise ValueError("Manager must belong to the same department.")
        
        if manager.user.role != UserRole.MANAGER:
            raise ValueError("Selected employee is not a manager.")
        
        if not manager.is_active:
            raise ValueError("Inactive employee cannot be a department manager.")
        
        department.manager = manager
        department.save(
            update_fields=["manager", "updated_at"]
        )

        return department
    
    @staticmethod
    def get_visible_departments(user, search=""):
        queryset = Department.objects.select_related(
            "manager",
            "manager__user",
        ).annotate(
            employee_count = Count("employees")
        )
        
        print("Current User:", user.username)
        print("Groups:", list(user.groups.values_list("name", flat=True)))
        if user.is_superuser:
            pass
        elif user.groups.filter(name="HR").exists():
            pass
        elif user.groups.filter(name="MANAGER").exists():
            queryset = queryset.filter(
                pk = user.employee_profile.department_id
            )
        else:
            queryset = queryset.filter(
                pk=user.employee_profile.department_id
            )

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search)
            )

        return queryset
    
    @staticmethod
    def get_visible_department(*, user, department_id):
        queryset = Department.objects.select_related(
            "manager",
            "manager__user",
        ).prefetch_related("employees__user",)

        if user.is_superuser:
            pass
        elif user.groups.filter(name="HR").exists():
            pass
        else:
            queryset = queryset.filter(
                pk=user.employee_profile.department_id
            )

        return queryset.filter(
            pk=department_id
        ).first()
    
    @staticmethod
    @transaction.atomic
    def update_department(*, department, validated_data):
        manager = validated_data.pop("manager", None)
        for field, value in validated_data.items():
            setattr(department, field, value)
        
        department.save()

        if manager != department.manager:
            if manager is None:
                department.manager = None
                department.save(update_fields=["manager", "updated_at"])
            else:
                DepartmentService.assign_manager(
                    department=department,
                    manager=manager,
                )

        return department
    
    @staticmethod
    @transaction.atomic
    def deactivate_department(*, department: Department):
        department.is_active = False
        department.manager = None

        department.save(
            update_fields=[
                "is_active",
                "manager",
                "updated_at",
            ]
        )

        return department