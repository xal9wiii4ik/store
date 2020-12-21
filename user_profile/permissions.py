from rest_framework.permissions import BasePermission


class IsStaffOrOwnerOnly(BasePermission):

    def has_permission(self, request, view):
        if len(request.path.split('/')) == 4:
            return bool(request.user.is_authenticated)
        return bool(
            request.user.is_authenticated and request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and (request.user.is_staff or (request.user == obj.user))
        )
