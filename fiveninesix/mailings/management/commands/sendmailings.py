import sys
import traceback

from django.core.management.base import BaseCommand, CommandError

from mailings.util import send_all

class Command(BaseCommand):
    help = 'Send all applicable mailings'

    def handle(self, *args, **options):
        """Send all applicable mailings"""
        try:
            recipients = send_all()
            self.stdout.write('mailings: sent to %d recipients.\n' % len(recipients))
        except Exception:
            traceback.print_exc(file=sys.stdout)
            raise CommandError('mailings: There was an exception while sending mailings')
