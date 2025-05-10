from django.core.management.base import BaseCommand
from django.core.management import call_command
import sys
import io

class Command(BaseCommand):
    help = 'Dump data with utf-8 encoding'

    def handle(self, *args, **kwargs):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        call_command('dumpdata', 'converter', indent=2, stdout=sys.stdout)


