from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Employee
from .services import EmployeeService

# Create your views here.
class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = "employees/list.html"
    context_object_name = "employees"
    paginate_by = 10

    def get_queryset(self):
        search_query = self.request.GET.get("search", "")

        return EmployeeService.get_visible_employees(
            user=self.request.user,
            search=search_query,
        )
        