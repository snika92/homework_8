from rest_framework.routers import SimpleRouter
from django.urls import path
from .apps import UsersConfig
from .views import UserViewSet, PaymentListApiView

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UserViewSet)

urlpatterns = [
path("payments/", PaymentListApiView.as_view(), name="payments_list"),
]

urlpatterns += router.urls
