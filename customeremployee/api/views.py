from django.utils import timezone
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Task
from .permissions import (IsCustomerOrSuperuser, IsEmployeeOrSuperuser, CanViewTask, CanAddCustomer, CanAddEmployee,
                          CanViewEmployees)
from .serializers import RegisterSerializer, UserSerializer, TaskSerializer


class CustomerRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated, IsEmployeeOrSuperuser, CanAddCustomer]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response

    def perform_create(self, serializer):
        serializer.save(role=User.CUSTOMER)


class EmployeeRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated, IsEmployeeOrSuperuser, CanAddEmployee]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response

    def perform_create(self, serializer):
        serializer.save(role=User.EMPLOYEE)


class EmployeeListView(generics.ListAPIView):
    queryset = User.employee.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsCustomerOrSuperuser, CanViewEmployees]


class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            if self.request.user.has_perm('api.can_create_task'):
                return [permissions.IsAuthenticated()]
            return [permissions.IsAuthenticated(), IsCustomerOrSuperuser()]
        elif self.action in ['assign', 'complete']:
            return [permissions.IsAuthenticated(), IsEmployeeOrSuperuser()]
        elif self.action == 'retrieve':
            if self.request.user.has_perm('api.can_view_all_tasks'):
                return [permissions.IsAuthenticated()]
            return [permissions.IsAuthenticated(), CanViewTask()]
        return super().get_permissions()

    def get_queryset(self):
        if self.action == 'list':
            user = self.request.user
            if user.has_perm('api.can_view_all_tasks'):
                return Task.objects.all()
            elif user.role == User.EMPLOYEE:
                return Task.objects.filter(employee=user) | Task.objects.filter(employee=None)
            elif user.role == User.CUSTOMER:
                return Task.objects.filter(customer=user)
        return Task.objects.all()

    @action(detail=True, methods=['patch'])
    def assign(self, request, pk=None):
        task = self.get_object()
        if task.status != Task.PENDING:
            return Response({'detail': 'Task is not pending'}, status=status.HTTP_400_BAD_REQUEST)
        task.employee = request.user
        task.status = Task.IN_PROGRESS
        task.save()
        return Response(TaskSerializer(task).data)

    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        task = self.get_object()

        if task.status != Task.IN_PROGRESS:
            return Response({'detail': 'Task is not in progress'}, status=status.HTTP_400_BAD_REQUEST)

        if 'report' not in request.data or not request.data['report']:
            return Response({'detail': 'Report is required to complete the task'}, status=status.HTTP_400_BAD_REQUEST)

        task.status = Task.COMPLETED
        task.report = request.data['report']
        task.closed_at = timezone.now()
        task.save()

        return Response(TaskSerializer(task).data)

    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied("Deleting tasks is not allowed.")
