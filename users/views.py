from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

from .models import User, Payment
from .serializers import UserSerializer, PaymentSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListApiView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_fields = ("course", "lesson", "method_of_payment",)
    filter_backends = [OrderingFilter]
    ordering_fields = ("date_of_payment",)
