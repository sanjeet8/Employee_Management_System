from django import forms

from apps.departments.models import Department
from .models import Employee, EmploymentType

class EmployeeAdminForm(forms.ModelForm):
    # ----- User fields -----
    username = forms.CharField(max_length=150)

    password = forms.CharField(
        widget=forms.PasswordInput(render_value=True)
    )

    first_name = forms.CharField(max_length=150)

    last_name = forms.CharField(max_length=150)

    email = forms.EmailField()

    class Meta:
        model = Employee

        fields = (
            "department",
            "manager",
            "joining_date",
            "employment_type",
            "salary",
            "is_active",
        )