from django.urls import path
from .views import DepartmentListView, DepartmentDetailView, DepartmentCreateView, DepartmentUpdateView, DepartmentDeactivateView

app_name = "departments"

urlpatterns = [
    path("", DepartmentListView.as_view(), name="department-list",),
    path("<int:pk>/", DepartmentDetailView.as_view(), name="department-detail"),
    path("create/", DepartmentCreateView.as_view(), name="department-create",),
    path("<int:pk>/edit/", DepartmentUpdateView.as_view(), name="department-update"),
    path("<int:pk>/deactivate/", DepartmentDeactivateView.as_view(), name="department-deactivate"),
]