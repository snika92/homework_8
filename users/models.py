from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from materials.models import Course, Lesson


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Введите Email")
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name="Телефон", help_text="Введите номер телефона")
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар",
                               help_text="Загрузите свой аватар")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Город", help_text="Введите город")
    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

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

    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="payments", verbose_name="Пользователь",
                             blank=True, null=True)
    date_of_payment = models.DateField(verbose_name="Дата оплаты", auto_now=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name="payments",
                               verbose_name="Курс")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="payments", blank=True, null=True,
                               verbose_name="Урок")
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты", default=0)
    method_of_payment = models.CharField(default=CARD, choices=PAYMENT_CHOICES, verbose_name="Метод оплаты")
    session_id = models.CharField(max_length=255, verbose_name="Id сессии", blank=True, null=True)
    link = models.URLField(max_length=400, verbose_name="Ссылка на оплату", blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["date_of_payment"]
