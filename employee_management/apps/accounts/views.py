from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from apps.departments.models import Department
from apps.employees.models import Employee

# Create your views here.
class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

class UserLogoutView(LogoutView):
    template_name = "accounts/login.html"

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        # Get the default context dictionary from TemplateView
        context =  super().get_context_data(**kwargs)

        context['employee_count'] = Employee.objects.count()
        context['department_count'] = Department.objects.count()

        return context