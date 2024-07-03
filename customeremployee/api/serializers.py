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
        queryset=User.objects.filter(role='customer'),
        source='customer',
        write_only=True,
        required=False
    )
    employee = UserSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='employee'),
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

        if user.role == 'customer':
            validated_data['customer'] = user
            if 'employee' in validated_data:
                raise serializers.ValidationError("Customers cannot assign employees to tasks.")
        elif user.role == 'employee':
            if 'customer' not in validated_data:
                raise serializers.ValidationError("Employees must assign a customer to the task.")
            if 'employee' in validated_data:
                raise serializers.ValidationError("You can assign a customer only after creation.")

        return Task.objects.create(**validated_data)
