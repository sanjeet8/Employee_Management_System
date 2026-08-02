from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView
from django.urls import reverse_lazy
from .models import Employee
from .services import EmployeeService
from apps.departments.models import Department
from apps.accounts.constants import UserRole
from .forms import EmployeeAdminForm
from apps.accounts.mixins import HRRequiredMixin
from django.views.generic import DetailView

# Create your views here.
class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = "employees/list.html"
    context_object_name = "employees"
    paginate_by = 10

    def get_queryset(self):
        search_query = self.request.GET.get("search", "")
        department_search = self.request.GET.get("department", "")

        return EmployeeService.get_visible_employees(
            user=self.request.user,
            search=search_query,
            department=department_search,
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['departments'] = Department.objects.all()
        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_params"] = query_params.urlencode()

        return context
    
class EmployeeCreateView(LoginRequiredMixin, HRRequiredMixin, FormView):
    template_name = "employees/create.html"
    form_class = EmployeeAdminForm
    success_url = reverse_lazy("employees:employees")

    def form_valid(self, form):
        EmployeeService.create_employee(
            **form.cleaned_data
        )
        return super().form_valid(form)
    
class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = "employees/detail.html"
    context_object_name = "employee"

    def get_queryset(self):
        return EmployeeService.get_visible_employees(
            user=self.request.user
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        employee = self.object
        
        is_hr = (
            user.is_superuser or
            user.groups.filter(name=UserRole.HR).exists()
        )

        permissions = {
            "can_view_salary": (
                is_hr or user == employee.user
            ),
            "can_edit": is_hr,
            "can_deactivate": is_hr,
        }

        context["permissions"] = permissions
        return context