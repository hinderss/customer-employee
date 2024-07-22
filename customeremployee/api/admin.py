from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from rest_framework.exceptions import ValidationError
from django import forms

from .models import User, Task


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'groups' in self.fields:
            self.fields['groups'].required = False
        if 'user_permissions' in self.fields:
            self.fields['user_permissions'].required = False

    def clean(self):
        cleaned_data = super().clean()
        user_permissions = cleaned_data.get('user_permissions')
        if user_permissions:
            for perm in user_permissions:
                try:
                    self.instance.validate_user_permission(perm)
                except ValidationError as e:
                    self.add_error('user_permissions', e)
        return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'groups' in self.fields:
            self.fields['groups'].required = False
        if 'user_permissions' in self.fields:
            self.fields['user_permissions'].required = False


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    search_fields = ('email',)
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'role')}),
        ('Permissions', {'fields': ('is_staff',)}),
        ('Groups and Permissions', {'fields': ('user_permissions',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'role')}),
        ('Permissions', {'fields': ('is_staff',)}),
        ('Groups and Permissions', {'fields': ('user_permissions',)}),
    )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['customer', 'employee', 'status', 'report']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.status == Task.COMPLETED:
            self.fields['report'].required = True

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        employee = cleaned_data.get('employee')
        report = cleaned_data.get('report')

        if status == Task.COMPLETED and not report:
            self.add_error('report', 'Report must be set when status is COMPLETED.')

        if status == Task.PENDING and employee:
            self.add_error('status', f'If employee is set, status should be {Task.IN_PROGRESS}.')

        return cleaned_data


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskForm
    fields = ['customer', 'employee', 'status', 'report']

