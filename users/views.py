from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.filters import OrderingFilter

from .models import User, Payment
from materials.models import Course, Lesson
from .permissions import IsUser
from .serializers import UserSerializer, PaymentSerializer, ShortUserSerializer
from .services import create_stripe_price, create_stripe_session, create_stripe_product
from django.shortcuts import get_object_or_404


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


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        course_id = self.request.data.get("course")
        if course_id:
            payment.course = get_object_or_404(Course, pk=course_id)
            product = payment.course.title
        else:
            lesson_id = self.request.data.get("lesson")
            payment.lesson = get_object_or_404(Lesson, pk=lesson_id)
            product = payment.lesson.title
        product_id = create_stripe_product(product)
        amount = self.request.data.get("amount")
        price = create_stripe_price(product_id, amount)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
