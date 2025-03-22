from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Payment, User

admin.site.register(User, UserAdmin)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "date_of_payment",
        "course",
        "lesson",
        "amount",
        "method_of_payment",
    )
    search_fields = (
        "user",
        "course",
        "lesson",
        "amount",
    )
    list_filter = (
        "user",
        "date_of_payment",
        "course",
        "lesson",
        "method_of_payment",
    )
