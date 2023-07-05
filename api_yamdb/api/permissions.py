from rest_framework import permissions


NOT_ALLOWED_TO_CHANGE = 'У вас недостаточно прав.'


class IsAdmin(permissions.BasePermission):
    message = NOT_ALLOWED_TO_CHANGE

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_staff
        )


class IsModeratorOrReadOnly(permissions.BasePermission):
    message = NOT_ALLOWED_TO_CHANGE

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_moderator
                or request.user == obj.author)


class IsAdminOrReadOnly(permissions.BasePermission):
    message = NOT_ALLOWED_TO_CHANGE

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user == obj.author)


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = NOT_ALLOWED_TO_CHANGE

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


