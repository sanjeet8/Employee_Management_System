from django.contrib import admin
from .models import Department

# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "created_at",)
    search_fields = ("name", "code",)
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("created_at", "updated_at")