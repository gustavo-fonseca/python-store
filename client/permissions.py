from rest_framework import permissions


class IsProfileOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return request.user and obj.pk == request.user.pk


