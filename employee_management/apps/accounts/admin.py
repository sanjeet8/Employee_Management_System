from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "employee_id",
        "role",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "employee_id",
    )

    ordering = (
        "employee_id",
    )

    def has_add_permission(self, request):
        return False