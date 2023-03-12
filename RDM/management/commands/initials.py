from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'load data'

    def handle(self, *args, **kwargs):
        call_command('loaddata', 'json/user.json')
        call_command('loaddata', 'json/RDM.json')
        