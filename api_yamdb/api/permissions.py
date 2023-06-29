from rest_framework.permissions import BasePermission


class ReviewCommentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        if request.method == "POST":
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        if request.user.is_authenticated and (
            request.user.role == "admin" or request.user.role == "moderator"
        ):
            return True
        if request.method == ("PATCH" or "DELETE"):
            return obj.author == request.user
