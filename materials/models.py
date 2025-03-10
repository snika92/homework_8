from django.db import models

from config import settings


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    image = models.ImageField(
        upload_to="images/", null=True, blank=True, verbose_name="Превью"
    )
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["title"]


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    image = models.ImageField(
        upload_to="images/", null=True, blank=True, verbose_name="Превью"
    )
    video = models.URLField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        related_name="lessons",
        null=True,
        blank=True,
        verbose_name="Курс",
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["title"]


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions",
                             verbose_name="Пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subscriptions",
                               verbose_name="Курс")

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ["user", "course"]
