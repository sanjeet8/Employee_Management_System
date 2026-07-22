from django.contrib.auth.models import UserManager
from django.db import transaction
from .constants import UserRole

class CustomUserManager(UserManager):
    
    @transaction.atomic
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        
        if not extra_fields.get("employee_id"):
            last_user = (
                self.select_for_update()
                .exclude(employee_id="")
                .order_by("-employee_id")
                .first()
            )
            if last_user:
                last_number = int(last_user.employee_id.replace("EMP", ""))
                employee_id = f"EMP{last_number + 1:05d}"
            else:
                employee_id = "EMP00001"

            extra_fields["employee_id"] = employee_id

        return super().create_user(
            username=username,
            password=password,
            **extra_fields,
        )
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", UserRole.ADMIN)

        return self.create_user(
            username=username,
            password=password,
            **extra_fields,
        )