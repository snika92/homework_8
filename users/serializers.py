from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from .models import User, Payment


class UserSerializer(ModelSerializer):
    payments = SerializerMethodField()

    def get_payments(self, user):
        return [payment.date_of_payment for payment in Payment.objects.filter(user=user)]

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "avatar", "city", "payments"]


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
