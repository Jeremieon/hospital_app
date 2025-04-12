from rest_framework.permissions import BasePermission
from .models import Doctor


class IsDoctor(BasePermission):
    """
    Custom permission to allow only doctors to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and belongs to the "Doctors" group
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Doctors").exists()
        )


from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsDoctorOrReadOnly(BasePermission):
    """
    Allow doctors full access, but restrict other users to read-only.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and Doctor.objects.filter(user=request.user).exists()
        )
