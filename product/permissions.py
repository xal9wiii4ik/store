from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrReadOnly(BasePermission):
    """Права для администратора и для чтения"""

    def has_permission(self, request, view):

        return bool(
            request.method in SAFE_METHODS or
            request.user.is_authenticated and request.user.is_staff
        )


class IsStaffOrOwnerOrShopOrReadOnly(BasePermission):
    """Права  для администратора и для чтения и для владельца"""

    def has_permission(self, request, view):

        return bool(
            request.method in SAFE_METHODS or
            request.user.is_authenticated and
            (request.user.is_staff or request.user.userprofile.is_shop)
        )

    def has_object_permission(self, request, view, obj):

        return bool(
            request.user.is_authenticated and
            (request.user.is_staff or (obj.user == request.user))
        )


class IsStaffOrOwner(BasePermission):
    """Права  для администратора и для чтения и для владельца"""

    def has_permission(self, request, view):

        return bool(
            request.method in SAFE_METHODS or
            request.user.is_authenticated and
            (request.user.is_staff or request.user.userprofile.is_shop)
        )

    def has_object_permission(self, request, view, obj):

        return bool(
            request.user.is_authenticated and
            (request.user.is_staff or (obj.product == request.user.product))
        )
