from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        if request.user.user_type == "customer":
            return request.method in permissions.SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        if request.user.user_type == "customer":
            return request.method in permissions.SAFE_METHODS
        return True


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.user_type == "customer"
        )


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.user_type == "employee"
        )
