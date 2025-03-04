from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

from .models import User, Payment
from .permissions import IsUser
from .serializers import UserSerializer, PaymentSerializer, ShortUserSerializer


# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = ShortUserSerializer


class UserRetrieveApiView(RetrieveAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.get_object() == self.request.user:
            return UserSerializer
        return ShortUserSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUser]


class UserDestroyApiView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUser]


class PaymentListApiView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_fields = ("course", "lesson", "method_of_payment",)
    filter_backends = [OrderingFilter]
    ordering_fields = ("date_of_payment",)
