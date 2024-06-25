from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

#henry做的
class IsLecturer(permissions.BasePermission):
    def has_permission(self, request, view):
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'Lecturer' in user_groups:
            return True
        return False

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'Student' in user_groups:
            return True
        return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'Administrator' in user_groups:
            return True
        return False
