from rest_framework import permissions


class IsAdminOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(request.method in permissions.SAFE_METHODS
                    or request.user == obj.author
                    or request.user.is_superuser)

    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS
                    or request.user.is_authenticated)


class IsAdminOrAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view):
        return bool(request.user == self.obj.author
                    or request.user.is_superuser)

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)
