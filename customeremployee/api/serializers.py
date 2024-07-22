from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User, Task


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'phone']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'role']


class TaskSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.customer.all(),
        source='customer',
        write_only=True,
        required=False
    )
    employee = UserSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.employee.all(),
        source='employee',
        write_only=True,
        required=False
    )

    class Meta:
        model = Task
        fields = ['id', 'customer', 'customer_id', 'employee', 'employee_id', 'status', 'created_at',
                  'updated_at', 'closed_at', 'report']
        read_only_fields = ['created_at', 'updated_at', 'closed_at', 'customer', 'report']

    def create(self, validated_data):
        validated_data['status'] = Task.PENDING
        user = self.context['request'].user

        if user.role == User.CUSTOMER:
            if user.has_perm('api.can_create_task') and ('customer' in validated_data):
                validated_data['customer'] = validated_data['customer']
            else:
                validated_data['customer'] = user
            if 'employee' in validated_data:
                raise serializers.ValidationError("Customers cannot assign employees to tasks.")
        elif user.role == User.EMPLOYEE:
            if 'employee' in validated_data:
                raise serializers.ValidationError("You can assign a employee only after creation.")
        if user.has_perm('api.can_create_task'):
            if 'customer' not in validated_data:
                raise serializers.ValidationError("Not customers must provide customer id to assign to the task.")

        return Task.objects.create(**validated_data)
