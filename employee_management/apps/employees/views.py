from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView
from django.urls import reverse_lazy
from .models import Employee
from .services import EmployeeService
from apps.departments.models import Department
from .forms import EmployeeAdminForm
from apps.accounts.mixins import HRRequiredMixin

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