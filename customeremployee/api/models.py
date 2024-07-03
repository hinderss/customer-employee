from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError

employee_permissions = (
    ('can_create_task', 'Can create task'),
    ('can_view_all_tasks', 'Can view all tasks'),
    ('can_add_customer', 'Can add customer'),
    ('can_add_employee', 'Can add employee'),
)

customer_permissions = (
    ('can_view_employees', 'Can view employees'),
)


class User(AbstractUser):
    EMPLOYEE = 'employee'
    CUSTOMER = 'customer'

    ROLE_CHOICES = [
        (EMPLOYEE, 'Employee'),
        (CUSTOMER, 'Customer'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, unique=True)

    class Meta:
        permissions = employee_permissions + customer_permissions

    def validate_user_permission(self, permission):
        if self.role == self.CUSTOMER:
            if permission.codename in [perm[0] for perm in employee_permissions]:
                raise ValidationError('Customers cannot have permission to create tasks,'
                                      ' view all tasks, or manage customers/employees.')

        if self.role == self.EMPLOYEE:
            if permission.codename == [perm[0] for perm in customer_permissions]:
                raise ValidationError('Employees cannot have customer-specific permissions.')


class Task(models.Model):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

    STATUS_CHOICES = [
        (PENDING, 'Ожидает исполнителя'),
        (IN_PROGRESS, 'В процессе'),
        (COMPLETED, 'Выполнена'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='created_tasks',
                                 on_delete=models.CASCADE,
                                 limit_choices_to={'role': 'customer'}
                                 )
    employee = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='assigned_tasks',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 limit_choices_to={'role': 'employee'}
                                 )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default=PENDING
                              )
    report = models.TextField(blank=True)
