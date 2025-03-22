from django.core.management.base import BaseCommand
from django.core.management import call_command
from materials.models import Course, Lesson


class Command(BaseCommand):
    help = 'Load materials from fixture'

    def handle(self, *args, **kwargs):
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        call_command('loaddata', 'materials.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
