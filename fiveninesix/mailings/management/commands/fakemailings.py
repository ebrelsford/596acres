import sys
import traceback

from django.core.management.base import BaseCommand, CommandError

from mailings.util import send_all

class Command(BaseCommand):
    help = 'Fake all applicable mailings'

    def handle(self, *args, **options):
        """
        Add delivery records for all applicable mailings, to keep them from 
        being sent to entities. Useful when adding mailings to an existing
        project and avoiding flooding users with emails that might be outdated.
        """
        try:
            recipients = send_all(fake=True)
            self.stdout.write('faked to %d recipients.\n' % len(recipients))
        except Exception:
            traceback.print_exc(file=sys.stdout)
            raise CommandError('There was an exception while faking mailings')
