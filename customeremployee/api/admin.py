from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from rest_framework.exceptions import ValidationError

from .models import User


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
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'groups' in self.fields:
            self.fields['groups'].required = False
        if 'user_permissions' in self.fields:
            self.fields['user_permissions'].required = False


class CustomUserAdmin(UserAdmin):
    model = User
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    search_fields = ('email',)
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
        ('Groups and Permissions', {'fields': ('user_permissions',), 'classes': ('collapse',)}),
    )


admin.site.register(User, CustomUserAdmin)
