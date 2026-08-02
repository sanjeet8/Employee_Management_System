from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from .constants import UserRole

class HRRequiredMixin(UserPassesTestMixin):
    """
    Allow access only to HR users and superusers.
    """
    def test_func(self):
        user = self.request.user
        return (
            user.is_superuser or
            user.groups.filter(name=UserRole.HR).exists()
        )
    
    def handle_no_permission(self):
        return PermissionDenied