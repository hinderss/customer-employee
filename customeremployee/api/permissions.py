from rest_framework.permissions import BasePermission
from .models import User


class CanAddCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('api.can_add_customer')


class CanViewEmployees(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('api.can_view_employees')


class CanAddEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('api.can_add_employee')


class IsCustomerOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.CUSTOMER or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user == obj.customer


class IsEmployeeOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.EMPLOYEE or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return obj.employee == request.user or obj.employee is None


class CanViewTask(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == User.CUSTOMER:
            return True
        elif request.user.role == User.EMPLOYEE:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == User.CUSTOMER:
            return obj.customer == request.user
        elif request.user.role == User.EMPLOYEE:
            return obj.employee == request.user or obj.employee is None
        return False
