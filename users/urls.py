from rest_framework.permissions import AllowAny
from django.urls import path
from .apps import UsersConfig
from .views import (PaymentListApiView, UserCreateAPIView, UserListApiView, UserRetrieveApiView, UserUpdateApiView,
                    UserDestroyApiView, PaymentCreateAPIView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

# router = SimpleRouter()
# router.register("", UserViewSet)

urlpatterns = [
    path('payments/', PaymentListApiView.as_view(), name='payments_list'),

    path('', UserListApiView.as_view(), name='users_list'),
    path('<int:pk>/', UserRetrieveApiView.as_view(), name='user_retrieve'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('<int:pk>/update/', UserUpdateApiView.as_view(), name="user_update"),
    path('<int:pk>/delete/', UserDestroyApiView.as_view(), name="user_delete"),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
]

# urlpatterns += router.urls
