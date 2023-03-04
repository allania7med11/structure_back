from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.all().update(password=make_password("admin"))
        self.stdout.write("Users password set to 'admin'")
