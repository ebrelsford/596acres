import sys
import traceback

from django.core.management.base import BaseCommand, CommandError

from mailreader.readers import NotesMailReader
from mailreader.util import get_mail

class Command(BaseCommand):
    help = 'Read mail and perform actions as specified by readers'

    readers = (
        NotesMailReader(),
    )

    def handle(self, *args, **options):
        """
        Read mail and perform actions as specified by readers.
        """
        self.stdout.write('mailreader: Running readmail')

        try:
            for mail in get_mail():
                for reader in self.readers:
                    if reader.should_read(**mail):
                        reader.read(verbose=True, **mail)
        except Exception:
            traceback.print_exc(file=sys.stdout)
            raise CommandError('mailreader: There was an exception while reading mail')

        self.stdout.write('mailreader: Done running readmail')
