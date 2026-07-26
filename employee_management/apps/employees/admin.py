from django.contrib import admin

from .models import Employee
from .forms import EmployeeAdminForm
from .services import EmployeeService

# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeAdminForm

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

    def save_form(self, request, obj, form, change):
        if change:
            return super().save_model(
                request,
                obj,
                form,
                change,
            )

        EmployeeService.create_employee(
            **form.cleaned_data
        )

    search_fields = ("user__username", "user__employee_id", "department__name",)

    list_filter = ("department", "employment_type", "is_active",)

    ordering = ("user__employee_id",)