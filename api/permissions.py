# imports
from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """
    Permission check for Super Admin role verification.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False


# class IsVerified(permissions.BasePermission):
#     """
#     Permission check for verified User.
#     """

#     def has_permission(self, request, view):
#         return request.user.is_verified
