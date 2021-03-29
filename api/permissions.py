from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user.is_administrator
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_administrator
        )


class IsOwnerAdminModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_administrator
            or request.user.is_moderator
        )
