from rest_framework import permissions

NOT_ALLOWED_TO_CHANGE = 'У вас недостаточно прав.'


class IsAdmin(permissions.BasePermission):
    """Доступ только для администратора."""

    message = NOT_ALLOWED_TO_CHANGE

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminOrReadOnly(IsAdmin):
    """Доступ для администратора или только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )


class IsAdminOrModeratorOrAuthorOrReadOnly(IsAdminOrReadOnly):
    """Доступ для администратора, модератора, автора или только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            super().has_permission(request, view)
            or request.user.is_moderator
            or obj.author == request.user
        )
