from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from .models import User, Payment


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email", "phone_number", "avatar", "city", "payments"]


class ShortUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "avatar", "city"]
