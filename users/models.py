from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from materials.models import Course, Lesson


class User(AbstractUser):
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите Email"
    )

    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите свой аватар",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Введите город",
    )

    token = models.CharField(
        max_length=100, verbose_name="Token", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Payment(models.Model):
    CASH = "Наличные"
    CARD = "Перевод на счёт"

    PAYMENT_CHOICES = [
        (CASH, "Наличные"),
        (CARD, "Перевод на счёт"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )
    date_of_payment = models.DateField(verbose_name="Дата оплаты")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Курс",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Урок",
    )
    payment_amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    method_of_payment = models.CharField(
        default=CARD, choices=PAYMENT_CHOICES, verbose_name="Метод оплаты"
    )

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["date_of_payment"]
