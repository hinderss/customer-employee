from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurrentUserView, TaskViewSet, CustomerRegisterView, EmployeeRegisterView, EmployeeListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/customer/', CustomerRegisterView.as_view(), name='customer_register'),
    path('register/employee/', EmployeeRegisterView.as_view(), name='employee_register'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('me/', CurrentUserView.as_view(), name='current_user'),
    path('tasks/create/', TaskViewSet.as_view({'post': 'create_task'}), name='task_create'),
    path('tasks/<int:pk>/assign/', TaskViewSet.as_view({'patch': 'assign'}), name='task_assign'),
    path('tasks/<int:pk>/complete/', TaskViewSet.as_view({'patch': 'complete'}), name='task_complete'),
]
