from django.urls import path
from .views import EmployeeListView, EmployeeCreateView, EmployeeDetailView, EmployeeUpdateView, EmployeeDeactivateView

app_name = "employees"

urlpatterns = [
    path("", EmployeeListView.as_view(), name="employees"),
    path("create/", EmployeeCreateView.as_view(), name="employee-create"),
    path("<int:pk>/", EmployeeDetailView.as_view(), name="employee-detail"),
    path("<int:pk>/edit", EmployeeUpdateView.as_view(), name="employee-update"),
    path("<int:pk>/deactivate", EmployeeDeactivateView.as_view(), name="employee-deactivate"),
]