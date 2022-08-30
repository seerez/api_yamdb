from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminOrSuperuserOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser


class AuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in SAFE_METHODS
                or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
                request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_superuser
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or request.user.username == obj.author.username
        )


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == 'admin'
                or request.user.is_superuser
        )
