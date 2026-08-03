from django import forms

from apps.departments.models import Department
from apps.accounts.constants import UserRole
from .models import Employee, EmploymentType

class EmployeeBaseForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)

    last_name = forms.CharField(max_length=150)

    email = forms.EmailField()

    role = forms.ChoiceField(
        choices = UserRole.choices
    )

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


class EmployeeCreateForm(EmployeeBaseForm):
    # ----- User fields -----
    username = forms.CharField(max_length=150)
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=True)
    )
    
    # For ordering
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.order_fields([
            "username",
            "password",
            "role",
            "first_name",
            "last_name",
            "email",
            "department",
            "manager",
            "joining_date",
            "employment_type",
            "salary",
            "is_active",
        ])


class EmployeeUpdateForm(EmployeeBaseForm):
    username = forms.CharField(
        disabled=True,
        required=False,
    )
    employee_id = forms.CharField(
        disabled=True,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        employee = self.instance

        if employee.pk:
            self.fields["username"].initial = employee.user.username
            self.fields["employee_id"].initial = employee.user.employee_id

            self.fields["first_name"].initial = employee.user.first_name
            self.fields["last_name"].initial = employee.user.last_name
            self.fields["email"].initial = employee.user.email
            self.fields["role"].initial = employee.user.role

        self.order_fields([
            "employee_id",
            "username",
            "role",
            "first_name",
            "last_name",
            "email",
            "department",
            "manager",
            "joining_date",
            "employment_type",
            "salary",
            "is_active",
        ])