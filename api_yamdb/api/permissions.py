from rest_framework import permissions

NOT_ALLOWED_TO_CHANGE = 'У вас недостаточно прав.'


class ReadOnly(permissions.BasePermission):
    """Доступ только для чтения."""

    message = NOT_ALLOWED_TO_CHANGE

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    """Доступ только для администратора."""

    message = NOT_ALLOWED_TO_CHANGE

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsModerator(permissions.BasePermission):
    """Доступ только для модератора."""

    message = NOT_ALLOWED_TO_CHANGE

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator


class IsAuthor(permissions.BasePermission):
    """Доступ только для автора."""

    message = NOT_ALLOWED_TO_CHANGE

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
