from rest_framework import permissions


class IsUserOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return (request.user and request.user.is_superuser) or (
            obj.user == request.user
        )

