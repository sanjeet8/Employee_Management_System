from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, FormView, UpdateView
from django.http import Http404
from django.shortcuts import redirect

from .models import Department
from .services import DepartmentService
from .forms import DepartmentForm, DepartmentUpdateForm
from apps.accounts.mixins import HRRequiredMixin

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
    

class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model=Department
    template_name="departments/detail.html"
    context_object_name="department"

    def get_object(self, queryset = None):
        department = DepartmentService.get_visible_department(
            user=self.request.user,
            department_id=self.kwargs["pk"],
        )

        if department is None:
            raise Http404("Department not found.")
        
        return department
    

class DepartmentCreateView(HRRequiredMixin, FormView):
    template_name = "departments/create.html"
    form_class = DepartmentForm

    def form_valid(self, form):
        DepartmentService.create_department(
            validated_data=form.cleaned_data.copy()
        )

        return redirect(
            "departments:department-list"
        )
    
class DepartmentUpdateView(HRRequiredMixin, UpdateView):
    model = Department
    template_name = "departments/update.html"
    form_class = DepartmentUpdateForm

    def form_valid(self, form):
        DepartmentService.update_department(
            department=self.object,
            validated_data=form.cleaned_data.copy(),
        )

        return redirect(
            "departments:department-detail",
            pk=self.object.pk,
        )