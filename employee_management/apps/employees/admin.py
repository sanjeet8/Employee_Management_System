from django.contrib import admin

from .models import Employee

# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "department",
        "manager",
        "employment_type",
        "joining_date",
        "salary",
        "is_active",
    )

    search_fields = ("user__username", "user__employee_id", "department__name",)

    list_filter = ("department", "employment_type", "is_active",)

    ordering = ("user__employee_id",)