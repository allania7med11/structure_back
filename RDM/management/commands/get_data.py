from django.core.management import call_command

class Command(BaseCommand):
    help = 'get data'

    def handle(self, *args, **kwargs):
        call_command('dumpdata', 'auth.user','-o','json/user.json','--indent','2')
        call_command('dumpdata', 'RDM','-o','json/RDM.json','--indent','2')