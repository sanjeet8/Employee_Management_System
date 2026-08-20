from django import forms

from .models import Department
from apps.employees.models import Employee
from apps.accounts.constants import UserRole

class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = (
            "name",
            "code",
            "description",
            "is_active",
        )

class DepartmentUpdateForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = (
            "name",
            "code",
            "description",
            "is_active",
            "manager",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["manager"].queryset = Employee.objects.filter(
            department=self.instance,
            user__role=UserRole.MANAGER,
            is_active=True,
        ).select_related("user")