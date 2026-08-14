from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from .constants import UserRole

class HRRequiredMixin(LoginRequiredMixin):
    """
    Allow access only to HR users and superusers.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        
        if (
            not request.user.is_superuser
            and not request.user.groups.filter(name="HR").exists()
        ):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)