from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Department
from .services import DepartmentService

class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = "departments/list.html"
    context_object_name = "departments"
    paginate_by = 10

    def get_queryset(self):
        search_query = self.request.GET.get("search", "")

        return DepartmentService.get_visible_departments(
            user=self.request.user,
            search=search_query,
        )
    

