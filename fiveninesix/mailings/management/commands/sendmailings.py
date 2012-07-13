import sys
import traceback

from django.core.management.base import BaseCommand, CommandError

from mailings.mailers import get_mailer_class
from mailings.models import DaysAfterWatcherOrganizerAddedMailing

from mailings.mailers import register_mailer, DaysAfterWatcherOrganizerAddedMailer
register_mailer(DaysAfterWatcherOrganizerAddedMailing, DaysAfterWatcherOrganizerAddedMailer)

class Command(BaseCommand):
    help = 'Send all applicable mailings'

    def handle(self, *args, **options):
        """Send all applicable mailings"""
        try:
            for mailing in DaysAfterWatcherOrganizerAddedMailing.objects.all():
                self.stdout.write('Sending DaysAfterAddedMailings')

                mailer_class = get_mailer_class(mailing)
                recipients = mailer_class(mailing).mail()
                self.stdout.write('sent to %d recipients.\n' % len(recipients))
        except Exception:
            traceback.print_exc(file=sys.stdout)
            raise CommandError('There was an exception while sending mailings')

