from django.core.management.base import BaseCommand
from django.core.management import call_command
from users.models import Payment


class Command(BaseCommand):
    help = 'Load payments from fixture'

    def handle(self, *args, **kwargs):
        Payment.objects.all().delete()
        call_command('loaddata', 'payments_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
