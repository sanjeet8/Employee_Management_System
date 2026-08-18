from django.urls import path
from .views import DepartmentListView

app_name = "departments"

urlpatterns = [
    path("", DepartmentListView.as_view(), name="department-list",),
]