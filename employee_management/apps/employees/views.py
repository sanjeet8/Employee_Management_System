from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Employee
from .services import EmployeeService
from apps.departments.models import Department

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

        return context