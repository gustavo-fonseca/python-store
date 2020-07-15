from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, SAFE_METHODS


class IsUserOwnerAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or (obj.user == request.user)


class IsAdminUserOrReadOnly(IsAdminUser):
    """
    Custom permission to only allow admin to edit, create and delete
    Regular users only can read
    """

    def has_permission(self, request, view):
        is_admin = super(IsAdminUserOrReadOnly, self).has_permission(
            request, view)
        return request.method in SAFE_METHODS or is_admin
